"""
Experiment 09: Association Rule Mining Using RapidMiner and Python (FP-Growth & Apriori)
Student: Bhavesh Punjabi | Roll No: 40 | Class: D15A
Subject: Data Mining and Business Intelligence (DMBI)
GitHub Folder Link: https://github.com/Sentry2311/DMBI_EXPERIMENTS/tree/main/Experiment_09_Association_Mining_RapidMiner
"""

import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
baskets_path = os.path.join(current_dir, "Exp9_Movie_Ticket_Baskets.csv")
df_baskets = pd.read_csv(baskets_path)

print("===== EXPERIMENT 9: MARKET BASKET ASSOCIATION MINING =====")
print(f"Total Transactions: {len(df_baskets)}")
print("\nFirst 5 Baskets:")
print(df_baskets.head())

# Transaction lists
transactions = [set(items.split(";")) for items in df_baskets["Items"]]

# Frequency calculation
from collections import Counter
from itertools import combinations

n = len(transactions)
min_sup = 0.10
item_counts = Counter(i for b in transactions for i in b)
freq_1 = {frozenset([i]): cnt for i, cnt in item_counts.items() if cnt / n >= min_sup}

print(f"\nTotal 1-itemsets meeting support >= {min_sup}: {len(freq_1)}")

# Generate frequent 2-itemsets
freq_2 = {}
items_list = list(freq_1.keys())
for a, b in combinations(items_list, 2):
    pair = a | b
    cnt = sum(pair.issubset(t) for t in transactions)
    if cnt / n >= min_sup:
        freq_2[pair] = cnt

print(f"Total 2-itemsets meeting support >= {min_sup}: {len(freq_2)}")

# Generate rules
rules = []
for pair, cnt in freq_2.items():
    sup_pair = cnt / n
    for item in pair:
        ant = frozenset([item])
        con = pair - ant
        conf = sup_pair / (freq_1[ant] / n)
        lift = conf / (freq_1[con] / n)
        if conf >= 0.40 and lift >= 1.0:
            rules.append({
                "Antecedent": list(ant)[0],
                "Consequent": list(con)[0],
                "Support": round(sup_pair, 3),
                "Confidence": round(conf, 3),
                "Lift": round(lift, 3)
            })

df_rules = pd.DataFrame(rules).sort_values("Confidence", ascending=False)
print(f"\nGenerated Association Rules (confidence >= 0.40, lift >= 1.0): {len(df_rules)}")
print(df_rules.head(10).to_string(index=False))
