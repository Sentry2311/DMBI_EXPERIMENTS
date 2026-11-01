"""
Experiment 06: Implementation of K-Means Clustering Using Python on Seeds Dataset
Student: Bhavesh Punjabi | Roll No: 40 | Class: D15A
Subject: Data Mining and Business Intelligence (DMBI)
GitHub Folder Link: https://github.com/Sentry2311/DMBI_EXPERIMENTS/tree/main/Experiment_06_KMeans_Clustering_Python
"""

import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score

current_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(current_dir, "seeds_7_features.csv"))

print("===== SEEDS DATASET OVERVIEW =====")
print(df.head())
print("\nDataset Shape:", df.shape)

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# Elbow method evaluation
print("\n===== ELBOW METHOD EVALUATION =====")
inertias = []
k_range = range(1, 11)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    print(f"K = {k:2d} | Inertia = {km.inertia_:10.4f}")

# Optimal K = 3
optimal_k = 3
km_opt = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
labels = km_opt.fit_predict(X_scaled)

sil_score = silhouette_score(X_scaled, labels)
db_score = davies_bouldin_score(X_scaled, labels)

print(f"\n===== CLUSTERING RESULTS (K = {optimal_k}) =====")
print(f"Silhouette Score     : {sil_score:.4f}")
print(f"Davies-Bouldin Index : {db_score:.4f}")

df["Cluster"] = labels
print("\nCluster Record Counts:")
print(df["Cluster"].value_counts().sort_index())

print("\nCluster Centroids (Original Measurement Units):")
print(df.groupby("Cluster").mean().round(4))
