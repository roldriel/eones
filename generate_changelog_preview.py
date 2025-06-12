import re
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SECTION_MAP = {
    "feat": "### Added",
    "fix": "### Fixed",
    "refactor": "### Changed",
    "perf": "### Changed",
    "docs": "### Documentation",
    "test": "### Tests",
    "chore": "### Maintenance",
    "style": "### Style",
    "ci": "### CI",
    "build": "### Build"
}

def get_commits_since(tag: str) -> list[dict]:
    log_cmd = [
        "git", "log", f"{tag}..HEAD",
        "--pretty=format:%H|%ad|%s",
        "--date=short"
    ]
    result = subprocess.run(log_cmd, capture_output=True, text=True, check=True)
    lines = result.stdout.strip().splitlines()
    commits = []
    for line in lines:
        commit_hash, date, message = line.split("|", 2)
        commits.append({
            "hash": commit_hash,
            "date": date,
            "message": message.strip()
        })
    # Ordenar por fecha (ascendente)
    return sorted(commits, key=lambda c: c["date"])


def classify_commit(message: str) -> str:
    match = re.match(r"^(\w+)(\(.+\))?:", message)
    if match:
        commit_type = match.group(1).lower()
        return SECTION_MAP.get(commit_type, "### Other")
    return "### Other"


def generate_changelog(commits: list[dict], output_file: Path) -> None:
    # Agrupar commits por sección
    grouped: dict[str, list[str]] = defaultdict(list)

    for c in commits:
        section = classify_commit(c["message"])
        formatted = f"- {c['message']} (`{c['hash'][:7]}`, {c['date']})"
        grouped[section].append(formatted)

    # Construir salida
    lines = [f"# Preview Changelog (since v1.0.0)\n"]
    lines.append(f"_Generated on {datetime.today().strftime('%Y-%m-%d')}_\n")

    for section in sorted(grouped.keys()):
        lines.append(f"\n{section}")
        lines.extend(grouped[section])

    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"[✔] Changelog generado en: {output_file}")


if __name__ == "__main__":
    output_path = Path("CHANGELOG.preview.md")
    try:
        commits = get_commits_since("v1.0.0")
        if not commits:
            print("[⚠] No se encontraron commits nuevos desde v1.0.0.")
        else:
            generate_changelog(commits, output_path)
    except subprocess.CalledProcessError as e:
        print(f"[✘] Error ejecutando git: {e}")
