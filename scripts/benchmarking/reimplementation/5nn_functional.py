"""
5nn_functional.py

Functional 5-nearest-neighbors (5NN) baseline using empirical substitution
fitness ("funsum_fitness_mean") for DMS score imputation.

Overview:
- For each gene, 10% of variants are held out as a test set.
- Missing DMS scores are imputed using the mean normalized DMS score of the
  5 most similar variants at the same position and wild-type residue.
- Similarity is defined as the negative absolute difference between
  substitution-level empirical fitness means.
- Performance is evaluated using per-gene Pearson correlation.

Input requirements:
- Preprocessed dataset produced by preprocess_5nn.py
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
# Input file must include:
#   - normalized_dms_score
#   - funsum_fitness_mean (empirical substitution-level fitness per gene)
DATA_FILE = "data/data-5nn-processed.csv"

# Output file: per-gene Pearson correlation coefficients
OUTPUT_FILE = "results/reimplementation/5nn_functional_mean_performance.csv"

# Fraction of variants per gene to hold out for testing
TEST_FRACTION = 0.10

# Random seed for reproducible train/test splits
RANDOM_SEED = 42

# ------------------------------------------------------------
# Load and validate input data
# ------------------------------------------------------------
data = pd.read_csv(DATA_FILE)

required_columns = {
    "gene_id",
    "mutation_id",
    "position",
    "wt_residue",
    "variant_residue",
    "normalized_dms_score",
    "funsum_fitness_mean",
}

missing = required_columns - set(data.columns)
if missing:
    raise ValueError(f"Missing required columns in {DATA_FILE}: {missing}")

# ------------------------------------------------------------
# 1. Per-gene train/test split (10% held out)
# ------------------------------------------------------------
# Each gene is split independently to avoid cross-gene leakage.
# At least one test variant is selected per gene when possible.
rng = np.random.default_rng(RANDOM_SEED)
data["is_test"] = False

for gene_id, idx in data.groupby("gene_id").groups.items():
    idx = np.asarray(list(idx))

    # Skip extremely small genes
    if len(idx) < 5:
        continue

    n_test = max(1, int(round(TEST_FRACTION * len(idx))))
    test_idx = rng.choice(idx, size=n_test, replace=False)
    data.loc[test_idx, "is_test"] = True

train = data.loc[~data["is_test"]].copy()
test = data.loc[data["is_test"]].copy()

# ------------------------------------------------------------
# 2. 5NN imputation using empirical substitution fitness
# ------------------------------------------------------------
# Neighbors are constrained to:
#   - same gene
#   - same residue position
#   - same wild-type amino acid
#
# Similarity metric:
#   similarity = -|funsum_i - funsum_target|
# (smaller difference → higher similarity)
def compute_similarity(f1, f2):
    """Return a similarity score where higher values indicate greater similarity."""
    return -abs(f1 - f2)

imputed_values = []

for _, row in test.iterrows():
    gene_id = row["gene_id"]
    position = row["position"]
    wt_residue = row["wt_residue"]
    target_funsum = row["funsum_fitness_mean"]

    # Candidate neighbors from the training set
    candidates = train[
        (train["gene_id"] == gene_id) &
        (train["position"] == position) &
        (train["wt_residue"] == wt_residue)
    ].copy()

    # Exclude the identical amino-acid substitution
    candidates = candidates[
        candidates["variant_residue"] != row["variant_residue"]
    ]

    if candidates.empty:
        imputed_values.append(np.nan)
        continue

    # Compute similarity to the target substitution
    candidates["similarity"] = candidates["funsum_fitness_mean"].apply(
        lambda x: compute_similarity(x, target_funsum)
    )

    candidates = candidates.dropna(subset=["similarity"])
    if candidates.empty:
        imputed_values.append(np.nan)
        continue

    # Select the top 5 most similar neighbors
    top5 = candidates.sort_values("similarity", ascending=False).head(5)

    # Impute as the mean normalized DMS score of the neighbors
    if top5["normalized_dms_score"].notna().sum() == 0:
        imputed_values.append(np.nan)
    else:
        imputed_values.append(top5["normalized_dms_score"].mean())
        # Alternative: use median instead of mean if desired

test["imputed_5nn_funsum"] = imputed_values

# ------------------------------------------------------------
# 3. Compute per-gene Pearson correlation
# ------------------------------------------------------------
results = []

for gene_id, df_gene in test.groupby("gene_id"):
    valid = df_gene.dropna(
        subset=["imputed_5nn_funsum", "normalized_dms_score"]
    )

    if len(valid) < 2:
        pearson = np.nan
    else:
        pearson, _ = pearsonr(
            valid["imputed_5nn_funsum"],
            valid["normalized_dms_score"],
        )

    results.append({
        "gene_id": gene_id,
        "5nn_funsum_pears": pearson,
    })

results_df = pd.DataFrame(results)

# ------------------------------------------------------------
# 4. Save results
# ------------------------------------------------------------
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
results_df.to_csv(OUTPUT_FILE, index=False)

print(f"✔ Saved FUNSUM 5NN benchmarking to {OUTPUT_FILE}")
