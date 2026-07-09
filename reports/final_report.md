# Final Project Report
## AI-Driven Predictive Maintenance System

**Author:** Isheka Singh
**Duration:** 6 Weeks
**Mentor:** Automation Lab
**Date:** [08-07-2026]

---

## 1. Project Overview
This project is an AI-based predictive maintenance system that predicts machine failures before they happen. It uses machine learning models trained on different industrial datasets such as CNC machines, aircraft engines, and wind turbines. The system also provides visual dashboards and a chatbot to help users understand the predictions. It was built to show how AI can reduce unexpected machine breakdowns and maintenance costs.

---

## 2. Problem Statement
Traditional maintenance is usually done after a machine breaks or on a fixed schedule. This can lead to unnecessary maintenance or unexpected failures that stop production. Predictive maintenance uses machine learning to detect problems early so maintenance can be done only when needed. This helps save time, money, and improves machine reliability.

---

## 3. Datasets

| Dataset | Source | Rows | Target |
|---|---|---|---|
| AI4I 2020 | Kaggle / UCI | 10,000 | Machine failure type |
| NASA CMAPSS FD001 | Kaggle / NASA | 20,631 | Remaining Useful Life |
| Wind Turbine SCADA | Kaggle | 50,473 | Anomaly detection |

---

## 4. Data Cleaning Summary
CNC Dataset

The dataset was checked for missing values and duplicate records. Column names were cleaned and data types were verified. The data was then prepared for feature engineering and model training.

Aircraft Engine Dataset

The engine dataset was cleaned by assigning proper column names and removing unused columns. Remaining Useful Life (RUL) values were calculated for each engine. The data was also prepared for both classification and regression models.

Wind Turbine Dataset

Missing values were removed and timestamp columns were converted into date and time format. Sensor readings were cleaned and new time-based features were created. The final dataset was prepared for anomaly detection.

---

## 5. EDA Key Findings

### CNC
- Failure rate: 3.39%
- Write 2 findings from your box plots and heatmap

### Aircraft Engine
- Mean RUL: 107.81 cycles
- Strongest predictors: cycle count, sensor_11, sensor_4
- Write 1 additional finding

### Wind Turbine
- Anomaly rate: 10%
- Write 2 findings from your power curve and monthly analysis

---

## 6. Feature Engineering

| Dataset | Features Added |
|---|---|
| CNC | temp_diff, power_proxy |
| Engine | failure_soon, 4 rolling means |
| Wind Turbine | power_deficit, efficiency, hour, season |

---

## 7. Models and Results

### CNC — Classification
| Model | F1 Score |
|---|---|
| Random Forest | 0.76 |
| Logistic Regression | 0.29 |
| XGBoost | 0.77 |

Best model: XGBoost

### Aircraft Engine — Classification
| Model | F1 Score |
|---|---|
| Random Forest | 0.88 |
| Logistic Regression | 0.82 |
| XGBoost | 0.888 |

Best model: XGBoost
RUL Regression — MAE: 25.32, R2: 0.717

### Wind Turbine — Classification
| Model | F1 Score |
|---|---|
| Random Forest | 1.0 |
| Logistic Regression | 1.0 |
| XGBoost | 0.99 |

Best model: Logistic Regression
Note: Perfect score because anomaly label was engineered from 
power_deficit — a feature used in training. Acknowledged limitation.

---

## 8. System Architecture
The project uses a Flask backend to run the machine learning models and process user requests. The frontend is built using HTML, CSS, and JavaScript to provide an easy-to-use interface. The frontend sends data to the Flask API, which returns predictions and results that are displayed on the webpage. The architecture diagram is provided in architecture.md.

---

## 9. Conversation History Feature
The application includes a chatbot that answers questions related to predictive maintenance, machine learning, and the project. Every conversation is stored temporarily during the current session so users can see previous messages. The history is cleared when the server restarts because it is not stored in a database.

---

## 10. API Endpoints Summary
GET / — Opens the main dashboard.
POST /predict/cnc — Predicts CNC machine failure.
POST /predict/engine — Predicts aircraft engine failure.
POST /predict/engine-rul — Predicts Remaining Useful Life (RUL).
POST /predict/wind — Detects wind turbine anomalies.
POST /chat — Answers project-related questions using the chatbot.
GET /history — Returns previous chatbot conversations.
---

## 11. Limitations

- CNC class imbalance (3.39% failures) — handled with class_weight but 
  more data would improve recall
- Wind turbine anomaly label is engineered not ground truth
- Chat answers are rule-based — not a true conversational AI
- Chat history resets on server restart — no persistent storage
- Engine feature array uses median values for sensors not in the UI

---

## 12. What I Learned
This project helped me understand the complete machine learning workflow, from cleaning data to deploying models in a web application. I learned how different datasets require different preprocessing and feature engineering techniques. I also improved my knowledge of Flask, APIs, HTML, CSS, JavaScript, and integrating machine learning models into a real application. While working on this project, I understood the importance of evaluating models carefully instead of only looking at accuracy. Overall, this project gave me practical experience in building an end-to-end AI application.
---

## 13. Conclusion
This project shows how machine learning can be used to predict equipment failures before they happen. It combines data analysis, predictive models, and a simple web application into one complete system. The project demonstrates the practical use of AI in industrial predictive maintenance and provides a strong foundation for future improvements.