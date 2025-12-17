"""
preprocess_5nn.py

Preprocessing script for the 5NN baseline dataset used in VEFill benchmarking.

This script:
1. Loads a mutation-level dataset that already contains BLOSUM100 scores.
2. Normalizes raw DMS scores using the VEFill normalization scheme.
3. Computes a per-gene, per-substitution average fitness score
   ("funsum_fitness_mean"), which serves as a substitution-level prior.
4. Writes the processed dataset to disk.

Expected input columns:
- gene_id
- mutation_id
- position
- wt_residue
- variant_residue
- blosum100
- wt_score              : wild-type reference score for the assay
- non_score             : nonsense (null) score for the assay
- dms_score             : raw DMS measurement
"""

import pandas as pd

# ------------------------------------------------------------
# Load input dataset
# ------------------------------------------------------------
# The input CSV must already include BLOSUM100 scores and all
# assay-specific reference values required for normalization.
input_path = "data/data-5nn.csv"
data = pd.read_csv(input_path)

# ------------------------------------------------------------
# Normalize DMS scores (VEFill normalization)
# ------------------------------------------------------------
# DMS scores are rescaled relative to the wild-type and nonsense
# references so that:
#   normalized_dms_score = 1   → wild type
#   normalized_dms_score = 0   → nonsense / null
#
# Formula:
# (dms_score - wt_score) / (wt_score - non_score) + 1
data["normalized_dms_score"] = (
    (data["dms_score"] - data["wt_score"]) /
    (data["wt_score"] - data["non_score"]) + 1.0
)

# ------------------------------------------------------------
# Compute substitution-level mean fitness (funsum_fitness_mean)
# ------------------------------------------------------------
# For each gene and amino-acid substitution (wt → variant),
# compute the mean normalized DMS score across all positions
# where that substitution occurs.
#
# This captures a gene-specific substitution effect that is
# independent of residue position.
data["funsum_fitness_mean"] = (
    data
    .groupby(["gene_id", "wt_residue", "variant_residue"])["normalized_dms_score"]
    .transform("mean")
)

# ------------------------------------------------------------
# Save processed dataset
# ------------------------------------------------------------
output_path = "data/data-5nn-processed.csv"
data.to_csv(output_path, index=False)

print(f"✔ Saved preprocessed file: {output_path}")
