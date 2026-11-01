"""
Experiment 07: K-Means Clustering Using RapidMiner Workflow Verification
Student: Bhavesh Punjabi | Roll No: 40 | Class: D15A
Subject: Data Mining and Business Intelligence (DMBI)
GitHub Folder Link: https://github.com/Sentry2311/DMBI_EXPERIMENTS/tree/main/Experiment_07_KMeans_Clustering_RapidMiner
"""

import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

current_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(current_dir, "seeds_7_features.csv"))

scaler = StandardScaler()
X_norm = scaler.fit_transform(df)

# K-Means k=3 matching RapidMiner parameters
km = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = km.fit_predict(X_norm)

df_norm = pd.DataFrame(X_norm, columns=df.columns)
df_norm["Cluster"] = [f"Cluster {l}" for l in labels]

print("===== RAPIDMINER NORMALIZED CENTROID TABLE =====")
centroids = df_norm.groupby("Cluster").mean()
print(centroids.round(4).to_string())

print("\n===== CLUSTER SIZE SUMMARY =====")
counts = df_norm["Cluster"].value_counts().sort_index()
total = len(df_norm)
for c, cnt in counts.items():
    print(f"{c:10} | Records: {cnt:3d} | Share: {cnt/total*100:5.1f}%")
