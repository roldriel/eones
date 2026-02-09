# 📟 Date Formatting

## Different output formats

```python
from eones import Eones
date = Eones("2024-12-25 15:30:00")

# Different output formats
print(date.format("%Y-%m-%d"))  # 2024-12-25
print(date.format("%d/%m/%Y"))  # 25/12/2024
print(date.format("%d %B %Y"))  # 25 December 2024
print(date.format("%H:%M:%S"))  # 15:30:00
```
