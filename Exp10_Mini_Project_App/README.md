# Experiment 10: Decision Support System & Interactive BI Dashboard (CA2 Mini Project)

Course: Data Mining and Business Intelligence (DMBI Lab) — Roll No. 38 (Sanjog Poojary).

---

## Overview

Experiment 10 encapsulates the full-stack **CA2 Mini Project**: an end-to-end Decision Support System (DSS) and Business Intelligence (BI) Dashboard for video streaming platform analytics. The application synthesizes core DMBI coursework modules into an interactive Streamlit web dashboard.

- **Report Document (DOCX):** [`EXP-10_DMBI_38_MiniProject_App.docx`](file:///c:/Users/Sanjog/Downloads/DMBI-Lab/Exp10_Mini_Project_App/EXP-10_DMBI_38_MiniProject_App.docx)
- **Report Document (PDF):** [`EXP-10_DMBI_38_MiniProject_App.pdf`](file:///c:/Users/Sanjog/Downloads/DMBI-Lab/Exp10_Mini_Project_App/EXP-10_DMBI_38_MiniProject_App.pdf)
- **Interactive Application Code:** [`CA2_Mini_Project/`](file:///c:/Users/Sanjog/Downloads/DMBI-Lab/CA2_Mini_Project)

---

## Coursework Modules Implemented

| Dashboard Page / Tab | DMBI Syllabus Module | Key Features & Algorithms |
|---|---|---|
| **1. Overview** | Module II: Data Preprocessing | Deduplication (515 raw $\rightarrow$ 502 clean rows), median imputation, watch duration capping at 300 min |
| **2. Warehouse & OLAP** | Module I: Data Warehousing | Star Schema (`Fact_Streams`, `Dim_User`, `Dim_Content`, `Dim_Device`), Roll-Up heatmap, Slice bar chart, Dice table |
| **3. Outliers** | Module IV: Outlier Analysis | Statistical IQR boxplot (2 outliers $> 208.5$ min), Isolation Forest ensemble (25 anomalies, contamination=0.05) |
| **4. Segments** | Module IV: Cluster Analysis | K-Means clustering ($k=2..7$), Silhouette score optimization (best $k=2$), 2D PCA cluster projection, cluster profiling |
| **5. Churn Model** | Module III: Classification | Decision Tree (CART), Gaussian Naïve Bayes, Random Forest with balanced class weights; confusion matrices; decision tree rules |
| **6. Recommendations** | Modules V & VI: Association Rules | Apriori frequent pattern mining, interactive confidence/lift sliders, personalized genre recommendation engine |

---

## How to Run the Mini Project App

### Option 1 — Batch Launcher (Windows)
Double-click [`run_app.bat`](file:///c:/Users/Sanjog/Downloads/DMBI-Lab/run_app.bat) in the repository root.

### Option 2 — Terminal Command
```bash
streamlit run CA2_Mini_Project/app/app.py
```
The application will launch automatically at `http://localhost:8501`.

---

## Analysis Pipeline Execution
To execute the automated analysis pipeline and regenerate all numerical metrics:
```bash
python CA2_Mini_Project/src/poc_pipeline.py
```
Outputs are saved to `CA2_Mini_Project/outputs/poc_results.json`.
