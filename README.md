# AI-Driven Predictive Maintenance System

Predict equipment failure before it happens using real sensor data and machine learning.

---

## Why This Project Exists

Unplanned equipment failure costs industries billions annually in downtime, repairs, and lost productivity. Traditional maintenance is either reactive (fix after failure) or time-based (fix on a schedule), both of which are inefficient.

This project builds a data-driven alternative: a system that continuously analyzes sensor readings from equipment and predicts failure before it occurs. The result is maintenance that happens exactly when needed — not too early, not too late.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Visualization | Plotly, Seaborn |
| Dashboard | Streamlit |
| Environment | Jupyter Notebook |
| Version Control | Git + GitHub |
| Deployment | Streamlit Cloud |

---

## Project Structure

```
predictive-maintenance/
|
├── data/
│   ├── readme.md/               
|
├── src/
│   ├── readme.md     # Data cleaning and feature engineering
│   
├── reports/
│   ├── readme.md/
│   
|
├── deployment/
│   └── readme.md            # Streamlit dashboard for live predictions
|
└── README.md
```

---

## How to Run

**1. Clone the repository**
```bash
git clone [https://github.com/your-username/predictive-maintenance.git](https://github.com/ishekaa12/predictive-maintenance-project.git)
cd predictive-maintenance-project
```


---

## Dataset

This project uses the NASA CMAPSS Turbofan Engine Degradation dataset, available on [Kaggle](https://www.kaggle.com/datasets/behrad3d/nasa-cmaps). Place the raw files inside `data/raw/` before running.

---

## Contributor

Developed independently as a 6-week project under the guidance of the Automation Lab.
