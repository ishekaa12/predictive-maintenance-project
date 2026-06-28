from flask import Flask, request, jsonify, render_template
import pickle
import os

app = Flask(__name__)

# Model storage — will be filled with real models in Week 3
models = {}

def load_models():
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    model_files = {
        "cnc": "cnc_model.pkl",
        "engine": "engine_model.pkl",
        "wind": "wind_model.pkl"
    }
    for name, filename in model_files.items():
        path = os.path.join(model_dir, filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                models[name] = pickle.load(f)
            print(f"Loaded model: {name}")
        else:
            print(f"Model not found yet: {name} — using placeholder")

load_models()
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "models_loaded": list(models.keys())
    })
    
@app.route("/predict/cnc", methods=["POST"])
def predict_cnc():
    data = request.get_json()

    # Validate required fields
    required = ["air_temp", "process_temp", "rotational_speed", 
                "torque", "tool_wear", "type"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Placeholder logic until real model is loaded in Week 3
    if "cnc" in models:
        # Real prediction — will wire up in Week 3
        prediction = models["cnc"].predict([[
            data["air_temp"], data["process_temp"],
            data["rotational_speed"], data["torque"], data["tool_wear"]
        ]])[0]
        probability = float(prediction)
    else:
        # Placeholder
        probability = 0.0

    return jsonify({
        "machine": "CNC Milling Machine",
        "failure_probability": probability,
        "failure_type": "Tool Wear Failure" if probability > 0.5 else "None",
        "risk_level": "HIGH" if probability > 0.7 else "MEDIUM" if probability > 0.4 else "LOW",
        "recommendation": "Schedule maintenance within 24 hours" if probability > 0.5 else "No action needed"
    })
@app.route("/predict/engine", methods=["POST"])
def predict_engine():
    data = request.get_json()

    if "cycle" not in data:
        return jsonify({"error": "Missing field: cycle"}), 400

    # Placeholder until Week 3
    rul = 100

    return jsonify({
        "machine": "Aircraft Engine",
        "rul_cycles": rul,
        "risk_level": "HIGH" if rul < 30 else "MEDIUM" if rul < 80 else "LOW",
        "recommendation": "Immediate inspection required" if rul < 30 else "Monitor closely" if rul < 80 else "Operating normally"
    })


@app.route("/predict/turbine", methods=["POST"])
def predict_turbine():
    data = request.get_json()

    required = ["wind_speed", "active_power", "theoretical_power"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Placeholder until Week 3
    power_deficit = data["theoretical_power"] - data["active_power"]
    anomaly = 1 if power_deficit > 500 else 0

    return jsonify({
        "machine": "Wind Turbine",
        "anomaly_detected": bool(anomaly),
        "power_deficit_kw": round(power_deficit, 2),
        "risk_level": "HIGH" if anomaly else "LOW",
        "recommendation": "Inspect turbine blades and generator" if anomaly else "Operating normally"
    })
if __name__ == "__main__":
    app.run(debug=True, port=5000)