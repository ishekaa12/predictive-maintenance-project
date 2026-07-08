import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix,
                             mean_absolute_error, r2_score)
from xgboost import XGBClassifier, XGBRegressor

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

print("Setup complete.")
#block 2 cnc model

# Load
cnc = pd.read_csv(os.path.join(DATA_DIR, "cnc_cleaned.csv"))

# Features and target
X_cnc = cnc[["air_temp_k", "process_temp_k", "rotational_speed_rpm",
              "torque_nm", "tool_wear_min", "temp_diff", "power_proxy"]]
y_cnc = cnc["machine_failure"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_cnc, y_cnc, test_size=0.2, random_state=42, stratify=y_cnc)

# Train three models
models_cnc = {
    "Random Forest": RandomForestClassifier(
        n_estimators=100, class_weight="balanced", random_state=42),
    "Logistic Regression": LogisticRegression(
        class_weight="balanced", max_iter=1000, random_state=42),
    "XGBoost": XGBClassifier(
        scale_pos_weight=int((y_cnc==0).sum()/(y_cnc==1).sum()),
        random_state=42, eval_metric="logloss")
}

print("=== CNC MODEL RESULTS ===")
best_cnc_score = 0
best_cnc_model = None
best_cnc_name = ""

for name, model in models_cnc.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    f1 = report["1"]["f1-score"]
    print(f"\n{name}")
    print(classification_report(y_test, y_pred))
    if f1 > best_cnc_score:
        best_cnc_score = f1
        best_cnc_model = model
        best_cnc_name = name

print(f"\nBest CNC model: {best_cnc_name} (F1: {round(best_cnc_score, 3)})")

# Save best model
with open(os.path.join(MODEL_DIR, "cnc_model.pkl"), "wb") as f:
    pickle.dump(best_cnc_model, f)
print("Saved cnc_model.pkl")


#bloack 3 engine model
# Load
engine = pd.read_csv(os.path.join(DATA_DIR, "engine_cleaned.csv"))

# Features and target — regression for RUL, classification for failure_soon
feature_cols = [col for col in engine.columns
                if col not in ["unit_id", "rul", "failure_soon"]]

X_eng = engine[feature_cols]
y_eng_reg = engine["rul"]
y_eng_cls = engine["failure_soon"]

# Split
X_train, X_test, y_train_r, y_test_r = train_test_split(
    X_eng, y_eng_reg, test_size=0.2, random_state=42)
_, _, y_train_c, y_test_c = train_test_split(
    X_eng, y_eng_cls, test_size=0.2, random_state=42)

# Classification models
models_eng = {
    "Random Forest": RandomForestClassifier(
        n_estimators=100, class_weight="balanced", random_state=42),
    "Logistic Regression": LogisticRegression(
        class_weight="balanced", max_iter=1000, random_state=42),
    "XGBoost": XGBClassifier(random_state=42, eval_metric="logloss")
}

print("=== ENGINE MODEL RESULTS ===")
best_eng_score = 0
best_eng_model = None
best_eng_name = ""

for name, model in models_eng.items():
    model.fit(X_train, y_train_c)
    y_pred = model.predict(X_test)
    report = classification_report(y_test_c, y_pred, output_dict=True)
    f1 = report["1"]["f1-score"]
    print(f"\n{name}")
    print(classification_report(y_test_c, y_pred))
    if f1 > best_eng_score:
        best_eng_score = f1
        best_eng_model = model
        best_eng_name = name

print(f"\nBest Engine model: {best_eng_name} (F1: {round(best_eng_score, 3)})")

# Also train XGBoost regressor for RUL number prediction
xgb_reg = XGBRegressor(n_estimators=100, random_state=42)
xgb_reg.fit(X_train, y_train_r)
rul_pred = xgb_reg.predict(X_test)
print(f"\nRUL Regression — MAE: {round(mean_absolute_error(y_test_r, rul_pred), 2)}")
print(f"RUL Regression — R2: {round(r2_score(y_test_r, rul_pred), 3)}")

# Save both
with open(os.path.join(MODEL_DIR, "engine_model.pkl"), "wb") as f:
    pickle.dump(best_eng_model, f)
with open(os.path.join(MODEL_DIR, "engine_rul_model.pkl"), "wb") as f:
    pickle.dump(xgb_reg, f)
print("Saved engine_model.pkl and engine_rul_model.pkl")



#block 4 wind turbine model
# Load
# Load
wind = pd.read_csv(os.path.join(DATA_DIR, "wind_cleaned.csv"))

# Features and target
feature_cols = ["wind_speed_ms", "active_power_kw", "theoretical_power_kwh",
                "wind_direction_deg", "power_deficit", "efficiency", 
                "hour", "season"]

X_wind = wind[feature_cols]
y_wind = wind["anomaly"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_wind, y_wind, test_size=0.2, random_state=42, stratify=y_wind)

# Train three models
models_wind = {
    "Random Forest": RandomForestClassifier(
        n_estimators=100, class_weight="balanced", random_state=42),
    "Logistic Regression": LogisticRegression(
        class_weight="balanced", max_iter=1000, random_state=42),
    "XGBoost": XGBClassifier(random_state=42, eval_metric="logloss")
}

print("=== WIND TURBINE MODEL RESULTS ===")
best_wind_score = 0
best_wind_model = None
best_wind_name = ""

for name, model in models_wind.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    f1 = report["1"]["f1-score"]
    print(f"\n{name}")
    print(classification_report(y_test, y_pred))
    if f1 > best_wind_score:
        best_wind_score = f1
        best_wind_model = model
        best_wind_name = name

print(f"\nBest Wind model: {best_wind_name} (F1: {round(best_wind_score, 3)})")

# Save best model
with open(os.path.join(MODEL_DIR, "wind_model.pkl"), "wb") as f:
    pickle.dump(best_wind_model, f)
print("Saved wind_model.pkl")
print("\n" + "="*50)
print("TRAINING COMPLETE — SUMMARY")
print("="*50)
print(f"CNC     — Best: {best_cnc_name:25} F1: {round(best_cnc_score, 3)}")
print(f"Engine  — Best: {best_eng_name:25} F1: {round(best_eng_score, 3)}")
print(f"Wind    — Best: {best_wind_name:25} F1: {round(best_wind_score, 3)}")
print("\nAll models saved to models/")