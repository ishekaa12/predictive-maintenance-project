# Reports

This folder contains all project documentation, analysis notebooks, and findings generated throughout the 6-week project.

---

## Structure

```
reports/
│
├── notebooks/
│   ├── 00_data_inspection.ipynb     # Raw inspection of all three datasets
│   ├── 01_data_cleaning.ipynb       # Full cleaning pipeline with before/after output
│   ├── 02_cnc_eda.ipynb             # Exploratory analysis — CNC Milling Machine
│   ├── 03_engine_eda.ipynb          # Exploratory analysis — Aircraft Engine
│   └── 04_turbine_eda.ipynb         # Exploratory analysis — Wind Turbine
│
├── figures/                         # Exported charts from EDA notebooks
│
├── data_cleaning_report.md          # Before/after summary for all three datasets
├── api_docs.md                      # Full Flask API endpoint documentation
└── architecture.md                  # System architecture and data flow diagram
```

---

## Documents

### data_cleaning_report.md
Documents every cleaning step applied to each dataset. Includes before and after snapshots — row counts, null counts, duplicate counts — and notes any issues to address during modeling such as class imbalance and engineered labels.

### api_docs.md
Documents all four Flask API endpoints. Includes input fields, output fields, example requests using curl, and example JSON responses. Reference this when wiring models into the backend in Week 5.

### architecture.md
Explains how the system components connect — browser, Flask server, ML models. Includes a text-based architecture diagram and a full walkthrough of one prediction request from input to output.

---

## Notebooks

Run notebooks in order. Each one depends on outputs from the previous.

| Notebook | Input | Output |
|---|---|---|
| 00_data_inspection | data/raw/ | Printed summaries |
| 01_data_cleaning | data/raw/ | data/processed/ CSVs |
| 02_cnc_eda | data/processed/cnc_cleaned.csv | Charts, feature ideas |
| 03_engine_eda | data/processed/engine_cleaned.csv | Charts, feature ideas |
| 04_turbine_eda | data/processed/wind_cleaned.csv | Charts, feature ideas |

---

## Status

| Document | Status |
|---|---|
| data_cleaning_report.md | Complete |
| api_docs.md | Complete |
| architecture.md | Complete |
| 00_data_inspection.ipynb | Complete |
| 01_data_cleaning.ipynb | Complete |
| 02_cnc_eda.ipynb | In progress — Week 2 |
| 03_engine_eda.ipynb | In progress — Week 2 |
| 04_turbine_eda.ipynb | In progress — Week 2 |
| figures/ | Populated during EDA |
