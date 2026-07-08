from pyexpat import features

from flask import Flask, request, jsonify, render_template
import pickle
import os
import pandas as pd
from pathlib import Path
from datetime import datetime

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"

app = Flask(__name__)
models = {}

def load_models():
    model_files = {
        "cnc": "cnc_model.pkl",
        "engine": "engine_model.pkl",
        "engine_rul": "engine_rul_model.pkl",
        "wind": "wind_model.pkl"
    }
    for name, filename in model_files.items():
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                models[name] = pickle.load(f)
            print(f"Loaded model: {name}")
        else:
            print(f"Model not found: {name}")

load_models()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "models_loaded": list(models.keys())})

@app.route("/predict/cnc", methods=["POST"])
def predict_cnc():
    data = request.get_json()

    required = ["air_temp", "process_temp", "rotational_speed", "torque", "tool_wear", "type"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    if "cnc" not in models:
        return jsonify({"error": "CNC model not loaded"}), 503

    try:
        air_temp = float(data["air_temp"])
        process_temp = float(data["process_temp"])
        rotational_speed = float(data["rotational_speed"])
        torque = float(data["torque"])
        tool_wear = float(data["tool_wear"])

        temp_diff = process_temp - air_temp
        power_proxy = torque * rotational_speed

        # Use DataFrame with column names — required for XGBoost
        features = pd.DataFrame([[air_temp, process_temp, rotational_speed,
                                   torque, tool_wear, temp_diff, power_proxy]],
                                 columns=["air_temp_k", "process_temp_k",
                                          "rotational_speed_rpm", "torque_nm",
                                          "tool_wear_min", "temp_diff", "power_proxy"])

        prediction = int(models["cnc"].predict(features)[0])
        probability = round(float(models["cnc"].predict_proba(features)[0][1]), 3)

        print(f"CNC DEBUG — prediction: {prediction}, probability: {probability}")

        if prediction == 1:
            if tool_wear > 200:
                failure_type = "Tool Wear Failure"
            elif temp_diff > 11:
                failure_type = "Heat Dissipation Failure"
            elif power_proxy > 80000:
                failure_type = "Overstrain Failure"
            else:
                failure_type = "Power Failure"
        else:
            failure_type = "None"

        risk_level = "HIGH" if probability > 0.7 else "MEDIUM" if probability > 0.4 else "LOW"
        recommendation = ("Schedule maintenance within 24 hours" if probability > 0.5
                          else "Monitor sensors closely" if probability > 0.3
                          else "No action needed")

        return jsonify({
            "machine": "CNC Milling Machine",
            "failure_probability": probability,
            "failure_type": failure_type,
            "risk_level": risk_level,
            "recommendation": recommendation
        })

    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid input value: {str(e)}"}), 422


@app.route("/predict/engine", methods=["POST"])
def predict_engine():
    data = request.get_json()

    if "cycle" not in data:
        return jsonify({"error": "Missing field: cycle"}), 400

    if "engine" not in models:
        return jsonify({"error": "Engine model not loaded"}), 503

    try:
        cycle = float(data["cycle"])
        s2 = float(data.get("sensor_2", 641.82))
        s3 = float(data.get("sensor_3", 1589.70))
        s4 = float(data.get("sensor_4", 1400.60))
        s7 = float(data.get("sensor_7", 554.36))
        s11 = float(data.get("sensor_11", 47.47))

        features = pd.DataFrame([[
            cycle, 0, 0,
            s2, s3, s4,
            21.61, s7, 534.0,
            534.0, s11, 522.0,
            2388.0, 8140.0, 8.44,
            392.0, 38.8, 23.3,
            s2, s7, s11, 522.0
     ]], columns=[
         "cycle", "op_setting_1", "op_setting_2",
         "sensor_2", "sensor_3", "sensor_4",
         "sensor_6", "sensor_7", "sensor_8",
         "sensor_9", "sensor_11", "sensor_12",
         "sensor_13", "sensor_14", "sensor_15",
         "sensor_17", "sensor_20", "sensor_21",
         "sensor_2_rolling", "sensor_7_rolling",
         "sensor_11_rolling", "sensor_12_rolling"
     ])

        failure_soon = int(models["engine"].predict(features)[0])
        rul = int(models["engine_rul"].predict(features)[0]) if "engine_rul" in models else 100

        print(f"ENGINE DEBUG — failure_soon: {failure_soon}, rul: {rul}")

        return jsonify({
            "machine": "Aircraft Engine",
            "failure_soon": bool(failure_soon),
            "rul_cycles": rul,
            "risk_level": "HIGH" if rul < 30 else "MEDIUM" if rul < 80 else "LOW",
            "recommendation": ("Immediate inspection required" if rul < 30
                               else "Monitor closely" if rul < 80
                               else "Operating normally")
        })

    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid input value: {str(e)}"}), 422


@app.route("/predict/turbine", methods=["POST"])
def predict_turbine():
    data = request.get_json()

    required = ["wind_speed", "active_power", "theoretical_power"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    if "wind" not in models:
        return jsonify({"error": "Wind model not loaded"}), 503

    try:
        wind_speed = float(data["wind_speed"])
        active_power = float(data["active_power"])
        theoretical_power = float(data["theoretical_power"])
        wind_direction = float(data.get("wind_direction", 180.0))

        power_deficit = theoretical_power - active_power
        efficiency = active_power / theoretical_power if theoretical_power > 0 else 0
        efficiency = max(0, min(1, efficiency))
        hour = 12
        season = 1

        features = pd.DataFrame([[
            wind_speed, active_power, theoretical_power,
            wind_direction, power_deficit, efficiency, hour, season
        ]], columns=["wind_speed_ms", "active_power_kw", "theoretical_power_kwh",
                     "wind_direction_deg", "power_deficit", "efficiency",
                     "hour", "season"])

        prediction = int(models["wind"].predict(features)[0])
        probability = round(float(models["wind"].predict_proba(features)[0][1]), 3)

        print(f"TURBINE DEBUG — prediction: {prediction}, probability: {probability}")

        return jsonify({
            "machine": "Wind Turbine",
            "anomaly_detected": bool(prediction),
            "failure_probability": probability,
            "power_deficit_kw": round(power_deficit, 2),
            "risk_level": "HIGH" if prediction == 1 else "LOW",
            "recommendation": ("Inspect turbine blades and generator" if prediction == 1
                               else "Operating normally")
        })

    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid input value: {str(e)}"}), 422


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405

chat_history = []

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Missing field: question"}), 400

    question = data["question"].strip()
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    answer = generate_answer(question)

    entry = {
        "id": len(chat_history) + 1,
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    chat_history.append(entry)

    return jsonify({
        "answer": answer,
        "history": chat_history
    })


@app.route("/chat/history", methods=["GET"])
def get_history():
    return jsonify(chat_history)


@app.route("/chat/clear", methods=["POST"])
def clear_history():
    chat_history.clear()
    return jsonify({"message": "Chat history cleared"})


def generate_answer(question):
    q = question.lower()

    if any(word in q for word in ["cnc", "milling", "tool wear", "torque", "spindle"]):
        return ("CNC Milling Machine failures are caused by tool wear, heat dissipation issues, "
                "power faults, or overstrain. The most common is tool wear — when the tool "
                "exceeds 200 minutes of use, failure probability increases significantly. "
                "Monitor torque and rotational speed alongside tool wear for early detection.")

    elif any(word in q for word in ["engine", "aircraft", "rul", "remaining", "turbofan", "cycle"]):
        return ("Aircraft engine health is measured using Remaining Useful Life (RUL) — "
                "the number of cycles left before failure. A RUL below 30 cycles signals "
                "immediate inspection. Key sensors to watch are sensor_11 (pressure), "
                "sensor_4 (temperature), and cycle count, which are the strongest predictors.")

    elif any(word in q for word in ["turbine", "wind", "power", "anomaly", "deficit", "scada"]):
        return ("Wind turbine anomalies occur when actual power output is significantly below "
                "theoretical power at the same wind speed. A power deficit above the 90th "
                "percentile with wind speed above 3 m/s indicates a likely fault in the "
                "blades, generator, or drivetrain. Efficiency ratio is the key metric.")

    elif any(word in q for word in ["model", "algorithm", "machine learning", "ml", "xgboost", "random forest"]):
        return ("This system uses three ML models: XGBoost for CNC failure classification, "
                "XGBoost for aircraft engine RUL regression and failure prediction, and "
                "Logistic Regression for wind turbine anomaly detection. Models were trained "
                "on cleaned sensor datasets with engineered features like temp_diff, "
                "power_proxy, rolling means, and efficiency ratio.")

    elif any(word in q for word in ["accuracy", "performance", "f1", "score", "result"]):
        return ("Model performance — CNC: XGBoost F1 score 0.77 on failure class. "
                "Aircraft Engine: XGBoost F1 score 0.888, RUL regression MAE 25.32 cycles. "
                "Wind Turbine: Logistic Regression F1 score 1.0 (anomaly label was "
                "engineered from power deficit threshold).")

    elif any(word in q for word in ["data", "dataset", "sensor", "training"]):
        return ("Three datasets were used: AI4I 2020 (10,000 CNC records), NASA CMAPSS FD001 "
                "(20,631 aircraft engine cycles), and Wind Turbine SCADA (50,473 readings). "
                "All datasets were cleaned, validated, and feature-engineered before training.")

    elif any(word in q for word in ["hello", "hi", "hey", "help"]):
        return ("Hello! I am the Predictive Maintenance assistant. You can ask me about "
                "any of the three machines — CNC Milling Machine, Aircraft Engine, or "
                "Wind Turbine — their failure patterns, sensor readings, model performance, "
                "or dataset details.")

    else:
        return ("I can answer questions about CNC machines, aircraft engines, wind turbines, "
                "the ML models used, dataset details, and model performance. "
                "Please ask about one of these topics.")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
