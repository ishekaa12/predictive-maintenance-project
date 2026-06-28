# API Documentation

## Base URL

```
http://localhost:5000
```

## Endpoints

---

### GET /

**Description:**
This endpoint opens the home page of the Predictive Maintenance Dashboard.

**Response:**
The user sees the web dashboard (`index.html`) where they can interact with the application.

---

### GET /health

**Description:**
This endpoint checks whether the API is running and shows which machine learning models have been loaded successfully.

**Example Response:**

```json
{
  "status": "ok",
  "models_loaded": []
}
```

> If the models are loaded, `models_loaded` may look like:

```json
{
  "status": "ok",
  "models_loaded": ["cnc", "engine", "wind"]
}
```

---

### POST /predict/cnc

**Description:**
Predicts the failure risk of a CNC Milling Machine using machine sensor values.

#### Request Body

| Field            | Type   | Description                        |
| ---------------- | ------ | ---------------------------------- |
| air_temp         | Number | Air temperature around the machine |
| process_temp     | Number | Process temperature                |
| rotational_speed | Number | Spindle rotational speed (RPM)     |
| torque           | Number | Machine torque                     |
| tool_wear        | Number | Tool wear value                    |
| type             | String | Machine type (required)            |

#### Example Request

```bash
curl -X POST http://localhost:5000/predict/cnc \
-H "Content-Type: application/json" \
-d '{
  "air_temp": 300,
  "process_temp": 310,
  "rotational_speed": 1500,
  "torque": 45,
  "tool_wear": 20,
  "type": "M"
}'
```

#### Example Response

```json
{
  "machine": "CNC Milling Machine",
  "failure_probability": 0.0,
  "failure_type": "None",
  "risk_level": "LOW",
  "recommendation": "No action needed"
}
```

---

### POST /predict/engine

**Description:**
Predicts the Remaining Useful Life (RUL) of an aircraft engine.

#### Request Body

| Field | Type   | Description                           |
| ----- | ------ | ------------------------------------- |
| cycle | Number | Current operating cycle of the engine |

#### Example Request

```bash
curl -X POST http://localhost:5000/predict/engine \
-H "Content-Type: application/json" \
-d '{
  "cycle": 120
}'
```

#### Example Response

```json
{
  "machine": "Aircraft Engine",
  "rul_cycles": 100,
  "risk_level": "LOW",
  "recommendation": "Operating normally"
}
```

---

### POST /predict/turbine

**Description:**
Detects whether a wind turbine is operating normally or if an anomaly is present.

#### Request Body

| Field             | Type   | Description            |
| ----------------- | ------ | ---------------------- |
| wind_speed        | Number | Current wind speed     |
| active_power      | Number | Actual power generated |
| theoretical_power | Number | Expected power output  |

#### Example Request

```bash
curl -X POST http://localhost:5000/predict/turbine \
-H "Content-Type: application/json" \
-d '{
  "wind_speed": 12.5,
  "active_power": 1800,
  "theoretical_power": 2400
}'
```

#### Example Response

```json
{
  "machine": "Wind Turbine",
  "anomaly_detected": true,
  "power_deficit_kw": 600,
  "risk_level": "HIGH",
  "recommendation": "Inspect turbine blades and generator"
}
```

---

## Error Handling

If a required field is missing from the request, the API returns a **400 Bad Request** error with a message showing which field is missing.

### Example

If the `tool_wear` field is not provided:

```json
{
  "error": "Missing field: tool_wear"
}
```

Another example:

```json
{
  "error": "Missing field: cycle"
}
```
