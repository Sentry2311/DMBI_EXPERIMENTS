"""
Experiment 05: Classification Using Python (Decision Tree & Naive Bayes)
Comparison: Inbuilt Library Functions vs User-Defined Custom Functions
Student: Bhavesh Punjabi | Roll No: 40 | Class: D15A
Subject: Data Mining and Business Intelligence (DMBI)
GitHub Folder Link: https://github.com/Sentry2311/DMBI_EXPERIMENTS/tree/main/Experiment_05_Classification_DecisionTree_NaiveBayes_Python
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, "student_result_classification_dataset.csv")
df = pd.read_csv(dataset_path)

print("===== STEP 1: DATASET OVERVIEW =====")
print(df.head(8))
print("\nClass balance:", df["Result_Category"].value_counts().to_dict())

# Preprocessing: Label Encoding
cat_cols = ["class", "section", "subject", "city"]
for col in cat_cols:
    df[col] = LabelEncoder().fit_transform(df[col])

feature_cols = ["age", "class", "section", "study_hours_per_week", "attendance_pct", "subject", "city"]
X = df[feature_cols].values
y = (df["Result_Category"] == "Pass").astype(int).values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ==============================================================================
# 1. INBUILT DECISION TREE CLASSIFIER
# ==============================================================================
dt_inbuilt_gini = DecisionTreeClassifier(criterion="gini", max_depth=5, random_state=42)
dt_inbuilt_gini.fit(X_train, y_train)
y_pred_dt_gini = dt_inbuilt_gini.predict(X_test)
acc_dt_gini = accuracy_score(y_test, y_pred_dt_gini)

dt_inbuilt_entropy = DecisionTreeClassifier(criterion="entropy", max_depth=5, random_state=42)
dt_inbuilt_entropy.fit(X_train, y_train)
y_pred_dt_entropy = dt_inbuilt_entropy.predict(X_test)
acc_dt_entropy = accuracy_score(y_test, y_pred_dt_entropy)

# ==============================================================================
# 2. USER-DEFINED (CUSTOM) DECISION TREE IMPLEMENTATION
# ==============================================================================
class CustomDecisionTreeNode:
    def __init__(self, depth=0, max_depth=5, criterion="gini"):
        self.depth = depth
        self.max_depth = max_depth
        self.criterion = criterion
        self.feature_idx = None
        self.threshold = None
        self.left = None
        self.right = None
        self.value = None

    def _impurity(self, y):
        if len(y) == 0: return 0
        p1 = np.mean(y)
        p0 = 1 - p1
        if self.criterion == "gini":
            return 1.0 - (p0**2 + p1**2)
        else: # entropy
            eps = 1e-12
            return -(p0 * np.log2(p0 + eps) + p1 * np.log2(p1 + eps))

    def fit(self, X, y):
        if self.depth >= self.max_depth or len(np.unique(y)) == 1 or len(y) < 4:
            self.value = 1 if np.mean(y) >= 0.5 else 0
            return

        best_gain = -1
        best_feat = None
        best_thresh = None
        current_imp = self._impurity(y)

        for f in range(X.shape[1]):
            thresholds = np.unique(X[:, f])
            for t in thresholds:
                left_mask = X[:, f] <= t
                right_mask = ~left_mask
                if left_mask.sum() == 0 or right_mask.sum() == 0:
                    continue
                w_left = left_mask.sum() / len(y)
                w_right = 1.0 - w_left
                gain = current_imp - (w_left * self._impurity(y[left_mask]) + w_right * self._impurity(y[right_mask]))
                if gain > best_gain:
                    best_gain = gain
                    best_feat = f
                    best_thresh = t

        if best_gain <= 0:
            self.value = 1 if np.mean(y) >= 0.5 else 0
            return

        self.feature_idx = best_feat
        self.threshold = best_thresh
        left_mask = X[:, best_feat] <= best_thresh

        self.left = CustomDecisionTreeNode(self.depth + 1, self.max_depth, self.criterion)
        self.left.fit(X[left_mask], y[left_mask])

        self.right = CustomDecisionTreeNode(self.depth + 1, self.max_depth, self.criterion)
        self.right.fit(X[~left_mask], y[~left_mask])

    def predict_one(self, x):
        if self.value is not None:
            return self.value
        if x[self.feature_idx] <= self.threshold:
            return self.left.predict_one(x)
        return self.right.predict_one(x)

    def predict(self, X):
        return np.array([self.predict_one(x) for x in X])

custom_dt = CustomDecisionTreeNode(max_depth=5, criterion="gini")
custom_dt.fit(X_train, y_train)
y_pred_custom_dt = custom_dt.predict(X_test)
acc_custom_dt = accuracy_score(y_test, y_pred_custom_dt)

# ==============================================================================
# 3. INBUILT NAIVE BAYES CLASSIFIER
# ==============================================================================
nb_inbuilt = GaussianNB()
nb_inbuilt.fit(X_train, y_train)
y_pred_nb = nb_inbuilt.predict(X_test)
acc_nb = accuracy_score(y_test, y_pred_nb)

# ==============================================================================
# 4. USER-DEFINED (CUSTOM) GAUSSIAN NAIVE BAYES IMPLEMENTATION
# ==============================================================================
class CustomGaussianNB:
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.priors = np.array([np.mean(y == c) for c in self.classes])
        self.means = np.array([X[y == c].mean(axis=0) for c in self.classes])
        self.vars = np.array([X[y == c].var(axis=0) + 1e-9 for c in self.classes])

    def _pdf(self, class_idx, x):
        mean = self.means[class_idx]
        var = self.vars[class_idx]
        numerator = np.exp(- (x - mean)**2 / (2 * var))
        denominator = np.sqrt(2 * np.pi * var)
        return numerator / denominator

    def predict(self, X):
        preds = []
        for x in X:
            posteriors = []
            for idx, c in enumerate(self.classes):
                prior = np.log(self.priors[idx])
                conditional = np.sum(np.log(self._pdf(idx, x) + 1e-12))
                posteriors.append(prior + conditional)
            preds.append(self.classes[np.argmax(posteriors)])
        return np.array(preds)

custom_nb = CustomGaussianNB()
custom_nb.fit(X_train, y_train)
y_pred_custom_nb = custom_nb.predict(X_test)
acc_custom_nb = accuracy_score(y_test, y_pred_custom_nb)

print("\n===== ACCURACY COMPARISON RESULTS =====")
print(f"Inbuilt Decision Tree (Gini)     : {acc_dt_gini*100:.2f}%")
print(f"Inbuilt Decision Tree (Entropy)  : {acc_dt_entropy*100:.2f}%")
print(f"Custom User-Defined Decision Tree: {acc_custom_dt*100:.2f}%")
print(f"Inbuilt Gaussian Naïve Bayes     : {acc_nb*100:.2f}%")
print(f"Custom User-Defined Naïve Bayes  : {acc_custom_nb*100:.2f}%")

print("\nClassification Report (Inbuilt Naïve Bayes):")
print(classification_report(y_test, y_pred_nb, target_names=["Fail", "Pass"]))
