"""
5nn_blosum100.py

5-nearest-neighbors (5NN) baseline for DMS score imputation using
BLOSUM100 substitution similarity.

Overview:
- Variants are split per gene into train (90%) and test (10%) sets.
- For each held-out variant, neighbors are restricted to variants with:
    * the same gene
    * the same residue position
    * the same wild-type amino acid
- Similarity between variants is defined by the BLOSUM100 score between
  their variant residues.
- The imputed DMS score is computed as the median normalized score of the
  top 5 most similar neighbors.
- Performance is evaluated using per-gene Pearson correlation.

Input requirements:
- A mutation-level dataset with raw or normalized DMS scores
- A BLOSUM100 matrix provided as a lookup table
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
DATA_FILE = "data/data-5nn-processed.csv"
# Must include at least:
#   gene_id, mutation_id, position, wt_residue, variant_residue,
#   wt_score, non_score, dms_score
#
# normalized_dms_score is computed if absent.

BLOSUM_FILE = "blosum100.csv"
# Expected columns:
#   amino_acid_x, amino_acid_y, blosum100

OUTPUT_FILE = "results/reimplementation/5nn_blosum100_performance.csv"

# Fraction of variants per gene used as test set
TEST_FRACTION = 0.10

# Random seed for reproducibility
RANDOM_SEED = 42

# ------------------------------------------------------------
# Load input data
# ------------------------------------------------------------
data = pd.read_csv(DATA_FILE)
blosum = pd.read_csv(BLOSUM_FILE)

# Validate required columns in the mutation dataset
required_cols = {
    "gene_id",
    "mutation_id",
    "position",
    "wt_residue",
    "variant_residue",
    "wt_score",
    "non_score",
    "dms_score",
}
missing = required_cols - set(data.columns)
if missing:
    raise ValueError(f"Missing required columns in {DATA_FILE}: {missing}")

# ------------------------------------------------------------
# 1. Normalize DMS scores (if not already present)
# ------------------------------------------------------------
# Normalization places wild type at 1 and nonsense at 0.
if "normalized_dms_score" not in data.columns:
    data["normalized_dms_score"] = (
        (data["dms_score"] - data["wt_score"]) /
        (data["wt_score"] - data["non_score"]) + 1.0
    )

# ------------------------------------------------------------
# 2. Prepare BLOSUM100 similarity lookup
# ------------------------------------------------------------
# The BLOSUM file is converted into a dictionary for fast lookup.
# Similarity is directional as provided in the input table.
blosum_lookup = {
    (row["amino_acid_x"], row["amino_acid_y"]): row["blosum100"]
    for _, row in blosum.iterrows()
}

def blosum_similarity(from_aa: str, to_aa: str) -> float:
    """
    Return the BLOSUM100 similarity score between two amino acids.
    Returns NaN if the pair is not present in the lookup table.
    """
    return blosum_lookup.get((from_aa, to_aa), np.nan)

# ------------------------------------------------------------
# 3. Per-gene train/test split (10% held out)
# ------------------------------------------------------------
rng = np.random.default_rng(RANDOM_SEED)
data["is_test"] = False

for gene_id, idx in data.groupby("gene_id").groups.items():
    idx = np.asarray(list(idx))

    # Skip genes with too few variants for meaningful evaluation
    if len(idx) < 2:
        continue

    n_test = max(1, int(round(TEST_FRACTION * len(idx))))
    test_idx = rng.choice(idx, size=n_test, replace=False)
    data.loc[test_idx, "is_test"] = True

train = data.loc[~data["is_test"]].copy()
test = data.loc[data["is_test"]].copy()

# ------------------------------------------------------------
# 4. 5NN imputation using BLOSUM100 similarity
# ------------------------------------------------------------
# For each test variant:
#   - Identify candidate neighbors from the training set with the same
#     (gene, position, wild-type residue).
#   - Compute BLOSUM100 similarity between variant residues.
#   - Select the top 5 most similar neighbors.
#   - Impute the score as the median normalized DMS score of those neighbors.
imputed_scores = []

for _, row in test.iterrows():
    gene_id = row["gene_id"]
    position = row["position"]
    wt_residue = row["wt_residue"]
    variant = row["variant_residue"]

    # Candidate neighbors from training data
    candidates = train[
        (train["gene_id"] == gene_id) &
        (train["position"] == position) &
        (train["wt_residue"] == wt_residue)
    ].copy()

    # Exclude the identical substitution, if present
    candidates = candidates[
        candidates["variant_residue"] != variant
    ]

    if candidates.empty:
        imputed_scores.append(np.nan)
        continue

    # Compute BLOSUM100 similarity to the target variant
    candidates["similarity"] = candidates["variant_residue"].apply(
        lambda aa: blosum_similarity(variant, aa)
    )

    # Remove candidates without a valid similarity score
    candidates = candidates.dropna(subset=["similarity"])
    if candidates.empty:
        imputed_scores.append(np.nan)
        continue

    # Select top 5 most similar neighbors
    neighbors = (
        candidates
        .sort_values("similarity", ascending=False)
        .head(5)
    )

    # Impute as the median normalized DMS score of neighbors
    if neighbors["normalized_dms_score"].notna().sum() == 0:
        imputed_scores.append(np.nan)
    else:
        imputed_scores.append(neighbors["normalized_dms_score"].median())

# Attach imputed values to the test set
test["imputed_5nn"] = imputed_scores

# ------------------------------------------------------------
# 5. Compute per-gene Pearson correlation
# ------------------------------------------------------------
performance = []

for gene_id, df_gene in test.groupby("gene_id"):
    valid = df_gene.dropna(
        subset=["imputed_5nn", "normalized_dms_score"]
    )

    if len(valid) < 2:
        pearson = np.nan
    else:
        pearson, _ = pearsonr(
            valid["imputed_5nn"],
            valid["normalized_dms_score"],
        )

    performance.append({
        "gene_id": gene_id,
        "5nn_pears": pearson,
    })

performance_df = pd.DataFrame(performance)

# ------------------------------------------------------------
# 6. Save results
# ------------------------------------------------------------
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
performance_df.to_csv(OUTPUT_FILE, index=False)

print(f"✔ Saved 5NN BLOSUM100 benchmarking results to {OUTPUT_FILE}")
