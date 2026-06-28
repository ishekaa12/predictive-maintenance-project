
# Deployment

## How to Run Locally

1. Clone the project repository.
2. Open a terminal and navigate to the project folder.
3. Move to the deployment folder:

```bash
cd deployment
```

4. Install the required Python packages (if not already installed):

```bash
pip install -r requirements.txt
```

5. Start the Flask application:

```bash
python3 app.py
```

6. Open your web browser and visit:

```text
http://127.0.0.1:5000
```

---

## File Structure

| File/Folder               | Description                                                                               |
| ------------------------- | ----------------------------------------------------------------------------------------- |
| `app.py`                  | Main Flask application that defines all API routes and loads the machine learning models. |
| `templates/index.html`    | Main web page displayed to the user.                                                      |
| `static/style.css`        | Stylesheet that controls the appearance of the dashboard.                                 |
| `static/script.js`        | Sends API requests and updates the webpage with prediction results.                       |
| `models/`                 | Stores the trained machine learning model (`.pkl`) files. *(Loaded when available.)*      |
| `reports/api_docs.md`     | Detailed documentation for all API endpoints.                                             |
| `reports/architecture.md` | Description of the system architecture and data flow.                                     |

---

## API Endpoints

| Endpoint                | Description                                                          |
| ----------------------- | -------------------------------------------------------------------- |
| `GET /`                 | Displays the Predictive Maintenance Dashboard.                       |
| `GET /health`           | Checks whether the API is running and shows which models are loaded. |
| `POST /predict/cnc`     | Predicts the maintenance risk of a CNC milling machine.              |
| `POST /predict/engine`  | Predicts the remaining useful life of an aircraft engine.            |
| `POST /predict/turbine` | Detects anomalies in a wind turbine.                                 |

For complete request and response details, see **`reports/api_docs.md`**.

---

## How to Deploy to Render

**To be completed in Week 6.**
