"""
Experiment 03: Exploratory Data Analysis and Visualization Using Python
Student: Bhavesh Punjabi | Roll No: 40 | Class: D15A
Subject: Data Mining and Business Intelligence (DMBI)
GitHub Folder Link: https://github.com/Sentry2311/DMBI_EXPERIMENTS/tree/main/Experiment_03_Exploratory_Data_Analysis_Visualization
"""

import os
import pandas as pd
import numpy as np

# Step 1: Loading Dataset and Initial Exploration
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, "Movie_Ticket_Booking_EDA_Dataset.csv")
df = pd.read_csv(dataset_path)

print("===== STEP 1: INITIAL DATA EXPLORATION =====")
print("Dataset Head:")
print(df.head(10))
print("\nDataset Info:")
print(df.info())
print("\nDataset Shape:", df.shape)

# Step 2: Task 1 - Statistical Measures of Central Tendency
print("\n===== STEP 2: MEASURES OF CENTRAL TENDENCY =====")
num_cols = ["Tickets", "Ticket_Price", "Total_Amount", "Booking_Rating"]
for col in num_cols:
    mean_val = df[col].mean()
    median_val = df[col].median()
    mode_val = df[col].mode()[0]
    print(f"{col:15} | Mean: {mean_val:8.2f} | Median: {median_val:8.2f} | Mode: {mode_val:8.2f}")

# Step 3: Task 2 - Statistical Measures of Dispersion
print("\n===== STEP 3: MEASURES OF DISPERSION =====")
for col in num_cols:
    std_val = df[col].std()
    var_val = df[col].var()
    range_val = df[col].max() - df[col].min()
    q75, q25 = np.percentile(df[col], [75, 25])
    iqr_val = q75 - q25
    print(f"{col:15} | Std: {std_val:8.2f} | Var: {var_val:8.2f} | Range: {range_val:8.2f} | IQR: {iqr_val:8.2f}")

# Step 4: Task 3 - Correlation Between Attributes
print("\n===== STEP 4: CORRELATION MATRIX =====")
corr_matrix = df[num_cols].corr()
print(corr_matrix.round(4))

# Step 5 to 9: Summary & Group Analysis
print("\n===== STEP 5: MOVIE & CITY WISE BOOKING ANALYSIS =====")
print("\nTotal Tickets Sold by Movie:")
print(df.groupby("Movie")["Tickets"].sum().sort_values(ascending=False))

print("\nTotal Revenue by City:")
print(df.groupby("City")["Total_Amount"].sum().sort_values(ascending=False))

print("\nAverage Rating by Movie:")
print(df.groupby("Movie")["Booking_Rating"].mean().round(2).sort_values(ascending=False))

print("\nEDA and Visual Analysis completed successfully.")
