# Flask Integration

Eones integrates with Flask by registering `eones_encoder` as the default JSON serializer. This allows `Eones`, `Date`, and `Delta` objects to be returned directly from routes.

## JSON Provider Configuration

Flask 2.2+ uses a JSON provider system. Override the `default` method to support Eones types:

```python
from flask import Flask
from eones.integrations.serializers import eones_encoder

app = Flask(__name__)
app.json.default = eones_encoder
```

With this configuration, any route that returns Eones objects via `jsonify` will serialize them automatically:

```python
from flask import jsonify
from eones import Eones
from eones.core.delta import Delta

@app.route("/now")
def now():
    return jsonify({"timestamp": Eones(), "uptime": Delta(hours=3)})
    # {"timestamp": "2025-06-15T10:00:00+00:00", "uptime": "PT3H"}
```

## Manual Serialization

For cases where you need explicit control, use `eones_encoder` with `json.dumps`:

```python
import json
from eones import Eones
from eones.integrations.serializers import eones_encoder

@app.route("/event")
def event():
    data = {"date": Eones("2025-12-25"), "name": "Holiday"}
    return app.response_class(
        json.dumps(data, default=eones_encoder),
        mimetype="application/json",
    )
```

## Request Parsing

Parse incoming date strings from request data into Eones objects:

```python
from flask import request
from eones import Eones

@app.route("/schedule", methods=["POST"])
def schedule():
    data = request.get_json()
    start = Eones(data["start_date"])
    end = Eones(data["end_date"])
    diff = start.difference(end, unit="days")
    return jsonify({"days": diff})
```
