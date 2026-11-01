"""
Experiment 08: Association Mining for Movie Ticket Bookings Using Apriori Algorithm
Student: Bhavesh Punjabi | Roll No: 40 | Class: D15A
Subject: Data Mining and Business Intelligence (DMBI)
GitHub Folder Link: https://github.com/Sentry2311/DMBI_EXPERIMENTS/tree/main/Experiment_08_Association_Mining_Apriori_Python
"""

import os
from itertools import combinations
from collections import Counter
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(current_dir, "Exp9_Movie_Ticket_Bookings.csv"))

print("===== STEP 1: MOVIE BOOKING DATASET =====")
print(f"Total Bookings: {len(df)}")
print(df.head(8))

# Convert to transaction baskets
transactions = []
for _, row in df.iterrows():
    basket = {
        f"Movie={row['Movie']}", f"Show={row['Show']}",
        f"Seat={row['Seat']}", f"Payment={row['Payment']}"
    }
    if row["Popcorn"]: basket.add("Snack=Popcorn")
    if row["Drink"]: basket.add("Snack=Drink")
    transactions.append(basket)

n = len(transactions)
min_support = 0.10

# Apriori algorithm
counts = Counter(item for basket in transactions for item in basket)
current = {frozenset([item]): count for item, count in counts.items() if count / n >= min_support}
frequent = dict(current)
k = 2
while current:
    candidates = set()
    prev = list(current)
    for a, b in combinations(prev, 2):
        union = a | b
        if len(union) == k and all(frozenset(s) in current for s in combinations(union, k-1)):
            candidates.add(union)
    next_level = {}
    for candidate in candidates:
        count = sum(candidate.issubset(b) for b in transactions)
        if count / n >= min_support:
            next_level[candidate] = count
    frequent.update(next_level)
    current = next_level
    k += 1

print(f"\nTotal Frequent Itemsets (min_support={min_support}): {len(frequent)}")

# Rule Generation
support_by_set = {items: count / n for items, count in frequent.items()}
rules = []
for itemset, joint_support in support_by_set.items():
    if len(itemset) < 2: continue
    for size in range(1, len(itemset)):
        for left_tuple in combinations(itemset, size):
            antecedent = frozenset(left_tuple)
            consequent = itemset - antecedent
            confidence = joint_support / support_by_set[antecedent]
            consequent_support = support_by_set[consequent]
            lift = confidence / consequent_support
            if confidence >= 0.40 and lift >= 1.0:
                rules.append({
                    "Antecedent": " + ".join(sorted(antecedent)),
                    "Consequent": " + ".join(sorted(consequent)),
                    "Support": joint_support,
                    "Confidence": confidence,
                    "Lift": lift
                })

rules_df = pd.DataFrame(rules).sort_values(["Confidence", "Lift"], ascending=False)
print(f"\nTotal Rules Generated (conf>=0.40, lift>=1.0): {len(rules_df)}")
print("\nTop 10 Association Rules:")
print(rules_df.head(10).to_string(index=False))
