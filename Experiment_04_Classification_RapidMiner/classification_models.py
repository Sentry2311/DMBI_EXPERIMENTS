"""
Experiment 04: Classification Model Comparison (Decision Tree & Naive Bayes)
Replicating RapidMiner Pipeline in Python
Student: Bhavesh Punjabi | Roll No: 40 | Class: D15A
Subject: Data Mining and Business Intelligence (DMBI)
GitHub Folder Link: https://github.com/Sentry2311/DMBI_EXPERIMENTS/tree/main/Experiment_04_Classification_RapidMiner
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

current_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(current_dir, "movie_ticket_booking_dataset.csv"))

print("Dataset Shape:", df.shape)
print("Target Distribution:\n", df["booking_status"].value_counts())

# Preprocessing & Encoding
cat_cols = ["Genre", "Show_Time", "Screen_Type", "Payment_Method"]
encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df[["Genre", "Show_Time", "Screen_Type", "Ticket_Price", "Tickets_Booked", "Customer_Age", "Payment_Method"]]
y = (df["booking_status"] == "Successful").astype(int)

# 80-20 Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 1. Decision Tree (Gini, max_depth=7)
dt = DecisionTreeClassifier(criterion="gini", max_depth=7, random_state=42)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
acc_dt = accuracy_score(y_test, y_pred_dt)

# 2. Naive Bayes
nb = CategoricalNB(min_categories=10)
nb.fit(X_train, y_train)
y_pred_nb = nb.predict(X_test)
acc_nb = accuracy_score(y_test, y_pred_nb)

print("\n===== CLASSIFICATION RESULTS =====")
print(f"Decision Tree Accuracy : {acc_dt*100:.2f}%")
print(f"Naïve Bayes Accuracy   : {acc_nb*100:.2f}%")

print("\nDecision Tree Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_dt))

print("\nNaïve Bayes Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_nb))
