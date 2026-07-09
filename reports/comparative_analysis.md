# Comparative Analysis of Predictive Maintenance Models

## 1. Overview
This report compares three classification models – **Logistic Regression (LR)**, **Random Forest (RF)**, and **XGBoost** – across three industrial assets: **CNC machine**, **Engine**, and **Wind Turbine**. The objective is to predict binary failure (class 1) 24 hours in advance. We evaluate models using **precision, recall, and F1-score** for the minority (failure) class, as accuracy is misleading due to class imbalance. Additionally, for the Engine, we include a **Remaining Useful Life (RUL)** regression model (MAE = 25.32, R² = 0.717).

---

## 2. Model Comparison per Machine

### 2.1 CNC Machine (Failure rate: 3.4%)

| Model               | Precision (class 1) | Recall (class 1) | F1-score (class 1) | Accuracy |
|---------------------|---------------------|------------------|--------------------|----------|
| Logistic Regression | 0.17                | 0.85             | **0.29**           | 0.86     |
| Random Forest       | 0.92                | 0.65             | **0.76**           | 0.99     |
| XGBoost             | 0.78                | 0.76             | **0.77**           | 0.98     |

**Winner: XGBoost** (F1 = 0.77)

**Analysis**:  
XGBoost edges out Random Forest by a small margin (0.77 vs. 0.76). Both tree-based models significantly outperform Logistic Regression. The CNC dataset has extreme class imbalance (only 3.4% failures) and complex, non-linear interactions between sensor readings (e.g., tool wear × vibration × temperature). XGBoost’s **gradient boosting** corrects sequential errors, allowing it to better separate the rare failure patterns. Random Forest comes close but tends to overfit the majority class slightly, as seen in its higher precision (0.92) but lower recall (0.65) – it is more conservative in flagging failures.

---

### 2.2 Engine (Failure rate: 15%)

| Model               | Precision (class 1) | Recall (class 1) | F1-score (class 1) | Accuracy |
|---------------------|---------------------|------------------|--------------------|----------|
| Logistic Regression | 0.73                | 0.95             | **0.82**           | 0.94     |
| Random Forest       | 0.91                | 0.85             | **0.88**           | 0.97     |
| XGBoost             | 0.91                | 0.86             | **0.888**          | 0.97     |

**Winner: XGBoost** (F1 = 0.888)

**Analysis**:  
XGBoost takes the lead by a hair (0.888 vs. 0.88). All three models perform reasonably well because the 15% failure rate provides enough positive examples for learning. Logistic Regression shows a **convergence warning** – it didn't fully converge after 1000 iterations, which suggests the data is not perfectly linearly separable; scaling or a different solver could improve it. Despite that, LR achieves a high recall (0.95) – meaning it catches 95% of true failures – at the cost of lower precision (0.73), i.e., many false alarms. XGBoost strikes a better balance, reducing false alarms while keeping recall high.

> **Note**: An additional RUL regression model was trained for the Engine, achieving **MAE = 25.32** (average prediction error in hours) and **R² = 0.717** – indicating that 71.7% of the variance in remaining life is explained by the features, which is a strong auxiliary signal for planning maintenance.

---

### 2.3 Wind Turbine (Failure rate: 10%)

| Model               | Precision (class 1) | Recall (class 1) | F1-score (class 1) | Accuracy |
|---------------------|---------------------|------------------|--------------------|----------|
| Logistic Regression | 1.00                | 1.00             | **1.00**           | 1.00     |
| Random Forest       | 1.00                | 1.00             | **1.00**           | 1.00     |
| XGBoost             | 0.99                | 0.99             | **0.99**           | 1.00     |

**Winner: Logistic Regression** (F1 = 1.00 – tied with Random Forest, but LR is simpler)

**Analysis**:  
All models achieve near‑perfect or perfect classification. LR wins because it is **simpler, faster, and interpretable** while matching the performance of complex ensembles. This suggests that the Wind Turbine dataset contains highly predictive, **linearly separable** features – likely gradual degradation trends (e.g., bearing temperature rate of change, power output deviations) that correlate strongly with failure. XGBoost slightly overfits (F1 = 0.99) on a few edge cases, but for practical purposes, any model would work. Since LR gives the same perfect score with less complexity, it is the recommended choice.

---

## 3. Why Logistic Regression Fails on CNC but Wins on Wind Turbine

| Aspect                | CNC                                      | Wind Turbine                            |
|-----------------------|------------------------------------------|-----------------------------------------|
| Failure mechanism     | Non-linear, multi‑factor interactions   | Gradual, linear degradation trends      |
| Class balance         | Severe imbalance (3.4%)                 | Moderate imbalance (10%)                |
| Feature space         | High‑dimensional, noisy, thresholds     | Clean, trending, strong linear signals  |
| LR performance        | F1 = 0.29 (disastrous)                  | F1 = 1.00 (perfect)                     |

**Why LR failed on CNC**:  
Logistic Regression assumes a linear decision boundary. On CNC, failures often occur when *multiple* conditions coincide (e.g., high temperature **and** low lubricant **and** high vibration). This is a logical AND‑type interaction that LR cannot capture without explicit interaction features. Additionally, the 3.4% failure rate biases LR toward the majority class – it tries to maximise accuracy by predicting "no failure" most of the time, leading to a **precision of just 0.17** (83% of its failure alerts are false alarms). Its recall (0.85) is decent, but the precision is so low that the model is unusable in practice.

**Why LR won on Wind Turbine**:  
Wind turbine failures are often driven by **monotonic degradation** – e.g., bearings heat up gradually, efficiency drops linearly with time. With proper feature engineering (rolling means, rate of change), the relationship between features and failure becomes approximately linear. The class balance (10%) is sufficient for LR to find a clear separating hyperplane. LR also benefits from being **regularised** (less overfitting) and gives maintenance engineers direct interpretability: *"a 2°C per hour rise in bearing temperature increases failure odds by X%."*

---

## 4. What Does an F1-score of 0.77 Mean in a Maintenance Context?

The CNC model achieves **F1 = 0.77** with the following breakdown (XGBoost):
- **Precision = 0.78** – 78% of the alerts are true failures.
- **Recall = 0.76** – 76% of actual failures are caught.

In plain numbers (assuming a test set of 2,000 samples, with 68 actual failures):
- True failures = 68
- Model catches ≈ 52 of them (recall 0.76)
- Misses ≈ 16 failures (false negatives)
- Issues ≈ 15 false alarms (since 52 / 0.78 ≈ 67 alerts total, so 15 false positives)

### Cost trade‑off: False Alarm vs. Missed Failure

| Cost Type          | Consequence                                                                 | Typical cost magnitude |
|--------------------|-----------------------------------------------------------------------------|------------------------|
| **False Alarm** (FP) | Unnecessary inspection, downtime, labour, parts replacement if done preemptively | Low–Medium (e.g., $500–$2,000) |
| **Missed Failure** (FN) | Unplanned breakdown, catastrophic damage, safety risk, emergency repair, production loss | High–Very High (e.g., $10,000–$100,000+) |

**Which is more costly?**  
In heavy industry, **a missed failure is almost always more expensive** than a false alarm. A sudden CNC spindle seizure can scrap expensive parts, damage the tool, and halt production for days. A false alarm might cost a technician's time for an inspection, but that is a controlled expense.

**Implication for F1 = 0.77**:  
An F1 of 0.77 is **acceptable only if the business accepts the 22% miss rate**. However, we should evaluate whether we can improve recall – even at the cost of more false alarms – by adjusting the classification threshold. If we lower the threshold to increase recall to 0.85, precision might drop to 0.65, giving F1 ≈ 0.74 but catching more true failures. Given the cost asymmetry, **we would prefer a higher recall over a higher precision**, even if F1 drops slightly. The current model (threshold=0.5) is reasonably balanced; but for CNC, we recommend **threshold tuning** to boost recall to ≥0.85.

---

## 5. Cross‑Machine Comparison & Impact of Class Balance

| Machine      | Failure Rate | Best Model       | Best F1 | Difficulty Rank |
|--------------|--------------|------------------|---------|-----------------|
| CNC          | 3.4%         | XGBoost          | 0.77    | Hardest (1)     |
| Engine       | 15%          | XGBoost          | 0.888   | Medium (2)      |
| Wind Turbine | 10%          | Logistic Reg.    | 1.00    | Easiest (3)     |

**Hardest machine**: **CNC**, by a significant margin. Its F1 is 0.77 compared to 0.888 for the Engine and perfect 1.0 for Wind.

**Why is CNC the hardest?**
1. **Extreme class imbalance** – only 3.4% failures. The model sees very few positive examples, so it struggles to learn the failure signature. Even with XGBoost's built‑in `scale_pos_weight`, the minority class remains sparse.
2. **Highly non‑linear failure modes** – tool wear, material inconsistencies, and coolant variations create complex, abrupt failure patterns that are hard to generalise from limited data.
3. **Noisy sensor environment** – CNC operations have high‑frequency vibrations and electromagnetic interference, which obscure the failure signal.

**How class balance affects model choice**:

| Imbalance Level | Example      | Recommended Models                               | Reason                                                                 |
|-----------------|--------------|--------------------------------------------------|------------------------------------------------------------------------|
| **Extreme** (≤5%) | CNC         | XGBoost, Random Forest (with class weights), SMOTE + any tree‑based | Tree‑based models handle non‑linearity and can focus on minority via weighting; LR fails due to linear boundary and bias. |
| **Moderate** (10–15%) | Engine, Wind | LR (if features are linear), RF, XGB – all viable | Sufficient positive examples allow LR to converge; ensembles give slight edge but interpretability may favour LR. |
| **Balanced** (>20%) | (not present) | Any model works; LR is fast and interpretable       | Class imbalance is no longer a major obstacle.                         |

- For **CNC**, even XGBoost barely reaches 0.77 – this suggests we need **more data** (more failure records) or a shift to **anomaly detection** (one‑class SVM) instead of supervised classification.
- For **Engine**, XGBoost is the winner but LR is not far behind (F1 0.82). If interpretability is critical, a well‑tuned LR with proper scaling could be acceptable.
- For **Wind Turbine**, LR is the clear champion – perfect performance and white‑box interpretability.

---

## 6. Conclusions & Recommendations

| Machine      | Recommended Model | F1 (failure class) | Actionable Next Steps                                                                 |
|--------------|-------------------|--------------------|---------------------------------------------------------------------------------------|
| CNC          | XGBoost           | 0.77               | Tune threshold to increase recall (target ≥0.85); collect more failure data; consider LSTM for time‑series. |
| Engine       | XGBoost           | 0.888              | Deploy XGBoost for classification; use RUL regression (R²=0.717) for predictive scheduling. |
| Wind Turbine | Logistic Reg.     | 1.00               | Deploy immediately – simplest, fastest, fully interpretable.                         |

**Overall best performer**: **XGBoost** wins on CNC and Engine, but Logistic Regression is unbeatable on Wind. The choice should balance **performance**, **interpretability**, and **deployment cost**.

**Key lesson**: *Class imbalance* and *linearity of the problem* are the two dominant factors dictating model selection – not the model family itself. Always inspect the confusion matrix and adjust the decision threshold based on the **cost of missed failures vs. false alarms**.

**Final thought**: An F1 of 0.77 on CNC is a solid baseline, but in a real maintenance setting, we would trade some precision for higher recall to avoid catastrophic breakdowns. The next iteration should implement **cost‑sensitive learning** that directly optimises for the expected maintenance cost, not just F1.

---

*Report generated from train.py outputs on 2026-07-09. All models and scalers are saved in the `models/` directory.*