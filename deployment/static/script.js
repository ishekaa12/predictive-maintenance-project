let currentMachine = "cnc";

function selectMachine(machine) {
    // Update active button
    document.querySelectorAll(".machine-btn").forEach(btn => btn.classList.remove("active"));
    event.target.classList.add("active");

    // Show correct form
    document.querySelectorAll(".machine-form").forEach(form => form.classList.remove("active"));
    document.getElementById("form-" + machine).classList.add("active");

    // Hide results
    document.getElementById("result").classList.add("hidden");

    currentMachine = machine;
}

function predict(machine) {
    let payload = {};

    if (machine === "cnc") {
        payload = {
            air_temp: parseFloat(document.getElementById("cnc-air-temp").value),
            process_temp: parseFloat(document.getElementById("cnc-process-temp").value),
            rotational_speed: parseInt(document.getElementById("cnc-speed").value),
            torque: parseFloat(document.getElementById("cnc-torque").value),
            tool_wear: parseInt(document.getElementById("cnc-wear").value),
            type: document.getElementById("cnc-type").value
        };
    } else if (machine === "engine") {
        payload = {
            cycle: parseInt(document.getElementById("engine-cycle").value),
            sensor_2: parseFloat(document.getElementById("engine-s2").value),
            sensor_3: parseFloat(document.getElementById("engine-s3").value),
            sensor_4: parseFloat(document.getElementById("engine-s4").value),
            sensor_7: parseFloat(document.getElementById("engine-s7").value),
            sensor_11: parseFloat(document.getElementById("engine-s11").value)
        };
    } else if (machine === "turbine") {
        payload = {
            wind_speed: parseFloat(document.getElementById("turbine-speed").value),
            active_power: parseFloat(document.getElementById("turbine-power").value),
            theoretical_power: parseFloat(document.getElementById("turbine-theoretical").value),
            wind_direction: parseFloat(document.getElementById("turbine-direction").value)
        };
    }

    fetch("/predict/" + machine, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => displayResult(data))
    .catch(error => console.error("Prediction error:", error));
}

function displayResult(data) {
    document.getElementById("result").classList.remove("hidden");

    document.getElementById("res-machine").textContent = data.machine || "—";

    const riskEl = document.getElementById("res-risk");
    riskEl.textContent = data.risk_level || "—";
    riskEl.className = "result-value risk-" + (data.risk_level || "");

    // Status line varies by machine type
    if (data.failure_type !== undefined) {
        document.getElementById("res-status").textContent = data.failure_type;
    } else if (data.rul_cycles !== undefined) {
        document.getElementById("res-status").textContent = data.rul_cycles + " cycles remaining";
    } else if (data.anomaly_detected !== undefined) {
        document.getElementById("res-status").textContent = data.anomaly_detected ? "Anomaly Detected" : "Normal";
    }

    document.getElementById("res-recommendation").textContent = data.recommendation || "—";
}