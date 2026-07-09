let currentMachine = "cnc";
const predictionLog = [];

function selectMachine(machine) {
    document.querySelectorAll(".machine-btn").forEach(btn => btn.classList.remove("active"));
    event.target.classList.add("active");

    document.querySelectorAll(".machine-form").forEach(form => form.classList.remove("active"));
    document.getElementById("form-" + machine).classList.add("active");

    document.getElementById("result").classList.add("hidden");

    currentMachine = machine;
}

function predict(machine) {
    const btn = document.querySelector(`#form-${machine} .predict-btn`);
    btn.textContent = "Running...";
    btn.disabled = true;

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
    .then(data => {
        displayResult(data);
        btn.textContent = "Run Prediction";
        btn.disabled = false;
    })
    .catch(error => {
        console.error("Prediction error:", error);
        btn.textContent = "Run Prediction";
        btn.disabled = false;
    });
}

function displayResult(data) {
    document.getElementById("result").classList.remove("hidden");

    document.getElementById("res-machine").textContent = data.machine || "—";

    const riskEl = document.getElementById("res-risk");
    riskEl.textContent = data.risk_level || "—";
    riskEl.className = "result-value risk-" + (data.risk_level || "");

    if (data.failure_type !== undefined) {
        document.getElementById("res-status").textContent = data.failure_type;
    } else if (data.rul_cycles !== undefined) {
        document.getElementById("res-status").textContent = data.rul_cycles + " cycles remaining";
    } else if (data.anomaly_detected !== undefined) {
        document.getElementById("res-status").textContent = data.anomaly_detected ? "Anomaly Detected" : "Normal";
    }

    document.getElementById("res-recommendation").textContent = data.recommendation || "—";

    // Update prediction log
    predictionLog.unshift({
        machine: data.machine,
        risk: data.risk_level,
        time: new Date().toLocaleTimeString()
    });

    const log = predictionLog.slice(0, 5);
    const logHTML = log.map(entry =>
        `<tr>
            <td>${entry.time}</td>
            <td>${entry.machine}</td>
            <td class="risk-${entry.risk}">${entry.risk}</td>
        </tr>`
    ).join("");

    document.getElementById("prediction-log").innerHTML = logHTML;
}

function sendChat() {
    const input = document.getElementById("chat-input");
    const question = input.value.trim();
    if (!question) return;

    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        const chatWindow = document.getElementById("chat-window");
        const empty = document.getElementById("chat-empty");
        if (empty) empty.remove();

        const entry = data.history[data.history.length - 1];

        const msg = document.createElement("div");
        msg.className = "chat-message";
        msg.innerHTML = `
            <div class="chat-question">${entry.question}</div>
            <div class="chat-answer">${entry.answer}</div>
            <div class="chat-timestamp">${entry.timestamp}</div>
        `;
        chatWindow.appendChild(msg);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    })
    .catch(error => console.error("Chat error:", error));
}