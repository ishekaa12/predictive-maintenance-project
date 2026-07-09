# API Testing Report

## Overview
Manual testing of all Flask API endpoints using curl. 
Conducted on: [07-0 7-2026]
Base URL: http://localhost:5000

---

## Test Results

### GET /
| Field | Detail |
|---|---|
| Expected | HTML dashboard page |
| Result | 200 OK |
| Status | Pass |

---

### GET /health
| Field | Detail |
|---|---|
| Input | None |
| Expected | JSON with status ok and models loaded |
| Result | { "models_loaded": ["cnc", "engine", "engine_rul", "wind"], "status": "ok" } |
| Status | Pass |

---

### POST /predict/cnc — Normal Conditions
| Field | Detail |
|---|---|
| Input | tool_wear: 7, torque: 42.8, rotational_speed: 1551 |
| Expected | Low failure probability |
| Result | failure_probability: 0.0, risk_level: LOW |
| Status | Pass |

### POST /predict/cnc — Failure Conditions
| Field | Detail |
|---|---|
| Input | tool_wear: 240, torque: 68.0, air_temp: 301.0 |
| Expected | High failure probability |
| Result | failure_probability: 1.0, risk_level: HIGH, failure_type: Tool Wear Failure |
| Status | Pass |

### POST /predict/cnc — Missing Field
| Field | Detail |
|---|---|
| Input | Missing torque field |
| Expected | 400 error with message |
| Result | { "error": "Missing field: torque" } |
| Status | Pass |

---

### POST /predict/engine — Normal Conditions
| Field | Detail |
|---|---|
| Input | cycle: 300, sensor readings at median values |
| Expected | RUL prediction and risk level |
| Result | rul_cycles: 158, risk_level: LOW, failure_soon: false |
| Status | Pass |

---

### POST /predict/turbine — Anomaly Conditions
| Field | Detail |
|---|---|
| Input | wind_speed: 12.0, active_power: 800, theoretical_power: 2800 |
| Expected | Anomaly detected, high power deficit |
| Result | anomaly_detected: true, power_deficit_kw: 2000.0, risk_level: HIGH |
| Status | Pass |

---

### POST /chat
| Field | Detail |
|---|---|
| Input | { "question": "Tell me about CNC failures" } |
| Expected | Relevant answer, entry saved to history |
| Result | Answer returned, history shows 1 entry with timestamp |
| Status | Pass |

### GET /chat/history
| Field | Detail |
|---|---|
| Input | None |
| Expected | Array of all past exchanges |
| Result | Array with id, question, answer, timestamp per entry |
| Status | Pass |

---

## Error Handling Tests

| Scenario | Expected Code | Result | Status |
|---|---|---|---|
| Missing required field | 400 | 400 returned with field name | Pass |
| Invalid data type | 422 | 422 returned with error message | Pass |
| Unknown endpoint | 404 | 404 returned with message | Pass |

---

## Summary

| Endpoint | Tests Run | Passed | Failed |
|---|---|---|---|
| GET / | 1 | 1 | 0 |
| GET /health | 1 | 1 | 0 |
| POST /predict/cnc | 3 | 3 | 0 |
| POST /predict/engine | 1 | 1 | 0 |
| POST /predict/turbine | 1 | 1 | 0 |
| POST /chat | 2 | 2 | 0 |
| GET /chat/history | 1 | 1 | 0 |
| Error handling | 3 | 3 | 0 |
| Total | 13 | 13 | 0 |