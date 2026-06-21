# Data Cleaning Report

## Overview

This report documents the data cleaning process for three datasets used in the 
AI-Driven Predictive Maintenance System. All cleaning was done using Python and 
Pandas. Cleaned files are saved in data/processed/.

---

## Dataset 1 — CNC Milling Machine (AI4I 2020)

### Before Cleaning
- Shape: 10,000 rows, 14 columns
- Null values: none
- Duplicate rows: none
- Concerns: Two columns (UDI, Product ID) were identifiers with no predictive 
  value. Column names had spaces and special characters.

### Actions Taken
- Dropped columns: UDI, Product ID
- Renamed all columns to lowercase with underscores for consistency

### After Cleaning
- Shape: 10,000 rows, 12 columns
- Null values: none
- Duplicate rows: none

---

## Dataset 2 — Wind Turbine SCADA

### Before Cleaning
- Shape: 50,530 rows, 5 columns
- Null values: none
- Duplicate rows: none
- Concerns: Date/Time column was stored as a string. LV ActivePower had 57 rows 
  with negative values which is physically impossible. No failure label existed.

### Actions Taken
- Converted Date/Time column from string to datetime format
- Removed 57 rows where active power was below zero
- Engineered a power_deficit column: difference between theoretical and actual power
- Engineered an anomaly column: flagged rows where power deficit exceeded the 
  90th percentile and wind speed was above 3 m/s

### After Cleaning
- Shape: 50,473 rows, 7 columns
- Null values: none
- Anomaly rate: [paste your anomaly rate here from wind["anomaly"].mean()]

---

## Dataset 3 — Aircraft Engine (NASA CMAPSS FD001)

### Before Cleaning
- Shape: 20,631 rows, 26 columns
- Null values: none
- Duplicate rows: none
- Concerns: No column names in the raw file. Four columns had zero variance 
  meaning the same value in every row. No prediction target column existed.

### Actions Taken
- Assigned column names manually based on NASA CMAPSS documentation
- Dropped 4 zero-variance columns which carry no information for ML
- Engineered RUL (Remaining Useful Life) column by subtracting current cycle 
  from the maximum cycle per engine unit

### After Cleaning
- Shape: 20,631 rows, 22 columns
- Null values: none
- RUL range: 0 to 191 cycles

---

## Summary

| Dataset         | Rows Before | Rows After | Cols Before | Cols After |
|-----------------|-------------|------------|-------------|------------|
| CNC             | 10,000      | 10,000     | 14          | 12         |
| Wind Turbine    | 50,530      | 50,473     | 5           | 7          |
| Aircraft Engine | 20,631      | 20,631     | 26          | 22         |

---

## Issues to Address in Modeling

- CNC dataset has class imbalance. Only 3.4% of rows are failures. The model 
  will need balancing techniques like SMOTE or class weighting.
- Wind turbine failure label is engineered not manually labeled. The 90th 
  percentile threshold is an assumption and may need tuning.
- Aircraft engine sensor_16 has near-zero variance and may be dropped during 
  feature selection in the modeling phase.
