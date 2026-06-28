# System Architecture

## Overview

The Predictive Maintenance Dashboard is a web application that allows users to enter machine sensor data and receive maintenance predictions. The system uses a Flask backend to process requests, machine learning models to generate predictions, and a web frontend built with HTML, CSS, and JavaScript to display the results.

---

## Architecture Diagram

```text
Client (Browser)
      |
      | HTTP GET /
      ↓
Flask Server (app.py)
      |
      | renders
      ↓
index.html + style.css + script.js
      |
      | User fills inputs and clicks Predict
      | HTTP POST /predict/cnc (JSON payload)
      ↓
Flask Route Handler
      |
      | loads
      ↓
ML Model (.pkl file)
      |
      | returns prediction
      ↓
JSON Response
      |
      | script.js updates the page
      ↓
Prediction displayed to the user
```

---

## Component Descriptions

### Flask Backend

The backend is written in **Flask** and is implemented in the `app.py` file. It handles all incoming requests from the frontend. The `/` route loads the main web page, the `/health` route checks whether the server and machine learning models are available, and the `/predict/cnc`, `/predict/engine`, and `/predict/turbine` routes receive input data, validate it, run the prediction (or placeholder logic), and return the results as JSON.

### Frontend

The frontend consists of three main files: `index.html`, `style.css`, and `script.js`. The `index.html` file creates the user interface where users enter machine data. The `style.css` file controls the appearance and layout of the application. The `script.js` file collects the user input, sends it to the Flask API using HTTP POST requests, receives the prediction results, and updates the webpage without reloading it.

### ML Models

The trained machine learning models are stored in the `models` folder as `.pkl` (pickle) files. When the Flask application starts, it checks whether these files exist and loads them into memory. The `.pkl` format is used because it allows trained Python machine learning models to be saved and loaded quickly without retraining them every time the application starts.

---

## Data Flow

A complete prediction request follows these steps:

1. The user opens the dashboard in a web browser.
2. The browser sends a **GET** request to `/`.
3. Flask returns the `index.html` page along with the CSS and JavaScript files.
4. The user enters machine sensor values into the form.
5. The user clicks the **Run Prediction** button.
6. JavaScript collects the input values from the form.
7. JavaScript sends a **POST** request with the data in JSON format to an endpoint such as `/predict/cnc`.
8. Flask receives the JSON data and checks that all required fields are present.
9. If the machine learning model is available, Flask uses the loaded `.pkl` model to generate a prediction. Otherwise, it uses the placeholder logic.
10. Flask creates a JSON response containing the prediction, risk level, and maintenance recommendation.
11. JavaScript receives the response from the server.
12. The webpage is updated instantly to display the prediction results to the user.