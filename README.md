# AI-Driven Predictive Maintenance System

Predict equipment failure before it happens using real sensor data and machine learning — across multiple machine types through a unified web dashboard.

---

## Why This Project Exists

Unplanned equipment failure costs industries billions annually in downtime, repairs, and lost productivity. Traditional maintenance is either reactive (fix after failure) or time-based (fix on a schedule), both of which are inefficient.

This project builds a data-driven alternative: a system that continuously analyzes sensor readings from equipment and predicts failure before it occurs. The result is maintenance that happens exactly when needed — not too early, not too late.

---

## Machines Covered

| Machine | Dataset | Prediction Target |
|---|---|---|
| CNC Milling Machine | AI4I 2020 (UCI / Kaggle) | Failure type — tool wear, heat, power, overstrain |
| Aircraft Engine | NASA CMAPSS FD001 (Kaggle) | Remaining Useful Life (RUL) in cycles |
| Wind Turbine | SCADA Dataset (Kaggle) | Anomaly detection via power deviation |

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Visualization | Plotly, Seaborn |
| Backend API | Flask |
| Frontend | HTML, CSS, JavaScript |
| Environment | Jupyter Notebook |
| Version Control | Git + GitHub |
| Deployment | Render |

---

## Project Structure

```
predictive-maintenance/
│
├── data/
│   ├── README.md                    # Data sources and column documentation
│   ├── raw/
│   │   ├── cnc/                     # AI4I 2020 original CSV
│   │   ├── aircraft_engine/         # NASA CMAPSS original TXT files
│   │   └── wind_turbine/            # SCADA original CSV
│   └── processed/
│       ├── cnc_cleaned.csv
│       ├── engine_cleaned.csv
│       └── wind_cleaned.csv
│
├── src/
│   ├── README.md                    # Source code documentation
│   ├── preprocess.py                # Data cleaning functions
│   ├── train.py                     # Model training for all three machines
│   ├── evaluate.py                  # Metrics and comparative analysis
│   └── predict.py                   # Inference on new sensor input
│
├── models/
│   ├── cnc_model.pkl
│   ├── engine_model.pkl
│   └── wind_model.pkl
│
├── reports/
│   ├── README.md
│   ├── api_docs.md                  # Full API endpoint documentation
│   ├── architecture.md              # System architecture and data flow
│   ├── data_cleaning_report.md      # Before and after cleaning summary
│   └── notebooks/
│       ├── 00_data_inspection.ipynb
│       ├── 01_data_cleaning.ipynb
│       ├── 02_cnc_eda.ipynb
│       ├── 03_engine_eda.ipynb
│       └── 04_turbine_eda.ipynb
│
├── deployment/
│   ├── README.md                    # How to run and deploy
│   ├── app.py                       # Flask backend server
│   ├── templates/
│   │   └── index.html               # Frontend dashboard
│   └── static/
│       ├── style.css
│       └── script.js
│
└── README.md
```

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/ishekaa12/predictive-maintenance-project.git
cd predictive-maintenance-project
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the Flask server**
```bash
cd deployment
python app.py
```

**4. Open the dashboard**
```
http://localhost:5000
```

**5. To retrain models**
```bash
python src/train.py
```

---

## Datasets

| Dataset | Source | Size |
|---|---|---|
| AI4I 2020 Predictive Maintenance | [Kaggle](https://www.kaggle.com/datasets/stephanmatzka/predictive-maintenance-dataset-ai4i-2020) | 10,000 rows |
| NASA CMAPSS FD001 | [Kaggle](https://www.kaggle.com/datasets/behrad3d/nasa-cmaps) | 20,631 rows |
| Wind Turbine SCADA | [Kaggle](https://www.kaggle.com/datasets/berkerisen/wind-turbine-scada-dataset) | 50,473 rows |

Place all raw files inside their respective folders under `data/raw/` before running.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the frontend dashboard |
| GET | `/health` | Returns server status and loaded models |
| POST | `/predict/cnc` | CNC failure prediction |
| POST | `/predict/engine` | Aircraft engine RUL prediction |
| POST | `/predict/turbine` | Wind turbine anomaly detection |

Full documentation in `reports/api_docs.md`

---

## Project Status

- [x] Week 1 — Data collection, cleaning, documentation
- [x] Week 2 — Flask API, frontend dashboard, architecture
- [ ] Week 3 — Model training
- [ ] Week 4 — Comparative analysis
- [ ] Week 5 — Model integration with Flask
- [ ] Week 6 — Deployment and final report

---

## Contributor

Developed independently as a 6-week project under the guidance of the Automation Lab.
