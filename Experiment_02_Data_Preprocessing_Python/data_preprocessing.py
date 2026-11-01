"""
Experiment 02: Data Preprocessing Using Python
Student: Bhavesh Punjabi | Roll No: 40 | Class: D15A
Subject: Data Mining and Business Intelligence (DMBI)
GitHub Folder Link: https://github.com/Sentry2311/DMBI_EXPERIMENTS/tree/main/Experiment_02_Data_Preprocessing_Python
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

# 1. Load Excel dataset
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "Movie_Ticket_Booking_Sample_Dataset.xlsx")
df = pd.read_excel(file_path)

print("===== ORIGINAL DATASET =====")
print(df.head(10))
print("\nDataset Shape:", df.shape)

# 2. Check missing values
print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

# 3. Handle missing numerical values
df["Age"] = df["Age"].fillna(df["Age"].mean())

# 4. Handle missing categorical values
df["Payment_Method"] = df["Payment_Method"].fillna(df["Payment_Method"].mode()[0])

print("\n===== MISSING VALUES AFTER HANDLING =====")
print(df.isnull().sum())

# 5. Check duplicates
print("\n===== DUPLICATES =====")
print("Duplicate rows before removal:", df.duplicated().sum())

# 6. Remove duplicates
df = df.drop_duplicates()
print("Duplicate rows after removal:", df.duplicated().sum())

# 7. Encode Gender
gender_encoder = LabelEncoder()
df["Gender"] = gender_encoder.fit_transform(df["Gender"])
print("\nGender Encoding Classes:", gender_encoder.classes_)

# 8. Encode Booking Status
status_encoder = LabelEncoder()
df["Booking_Status"] = status_encoder.fit_transform(df["Booking_Status"])
print("Booking Status Encoding Classes:", status_encoder.classes_)

# 9. Select numerical columns for scaling
numerical_columns = ["Age", "Tickets", "Ticket_Price", "Total_Amount"]

# 10. Feature scaling using StandardScaler
scaler = StandardScaler()
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# 11. Display final preprocessed dataset
print("\n===== FINAL PREPROCESSED DATASET (Normalized) =====")
print(df.head(10))

# 12. Final verification
print("\n===== FINAL CHECK =====")
print("Missing values count:\n", df.isnull().sum())
print("Duplicate rows count:", df.duplicated().sum())

# 13. Save preprocessed dataset
output_file = os.path.join(current_dir, "Preprocessed_Movie_Ticket_Booking.xlsx")
df.to_excel(output_file, index=False)
print(f"\nPreprocessed dataset successfully saved to: {output_file}")
