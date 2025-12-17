"""
noise_simulation.py

Estimate per-gene noise ceilings for Deep Mutational Scanning (DMS) datasets
using a Monte Carlo noise injection procedure.

Concept:
- Each variant has an associated experimental uncertainty (sigma).
- We simulate repeated noisy realizations of the observed DMS scores by
  adding Gaussian noise with variance sigma^2.
- The Pearson correlation between the original scores and their noisy
  realizations defines an upper bound ("noise ceiling") on achievable
  predictive performance.

Output:
- Mean, median, and percentile bounds of the expected Pearson r per gene.
- These values represent assay-intrinsic limits rather than model performance.
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from tqdm import tqdm

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
DATA_FILE = "data/domainome_preprocessed_with_sigma_and_score.csv"

# Output file containing per-gene noise ceiling statistics
OUTPUT_FILE = "results/noise_simulation/noise_ceiling_per_gene.csv"

# Number of Monte Carlo replicates per gene
# Chosen to be stable while remaining computationally tractable
N_REPLICATES = 300

# Random seed for reproducibility
RANDOM_SEED = 42

# ---------------------------------------------------------
# Load and validate input data
# ---------------------------------------------------------
df = pd.read_csv(DATA_FILE)

required_cols = {"gene_id", "dms_score", "sigma"}
missing = required_cols - set(df.columns)
if missing:
    raise ValueError(
        f"Missing required columns {missing} in {DATA_FILE}"
    )

rng = np.random.default_rng(RANDOM_SEED)

# ---------------------------------------------------------
# Function: compute noise ceiling for a single gene
# ---------------------------------------------------------
def compute_noise_ceiling_for_gene(sub):
    """
    Compute Monte Carlo estimates of the noise ceiling for one gene.

    Parameters:
        sub (pd.DataFrame): Subset of rows corresponding to one gene.
                            Must contain 'dms_score' and 'sigma'.

    Returns:
        pd.Series with summary statistics of the Pearson r distribution,
        or None if the noise ceiling is not well-defined.
    """
    y = sub["dms_score"].values
    sigma = sub["sigma"].values

    # If sigma is missing or identically zero, the noise ceiling is undefined
    if np.isnan(sigma).all() or np.all(sigma == 0):
        return None

    r_vals = []

    for _ in range(N_REPLICATES):
        # Generate one noisy realization of the DMS scores
        noise = rng.normal(loc=0.0, scale=sigma)
        y_noisy = y + noise

        # Pearson r is undefined if either vector lacks variance
        if len(np.unique(y)) < 2 or len(np.unique(y_noisy)) < 2:
            r_vals.append(np.nan)
            continue

        r, _ = pearsonr(y, y_noisy)
        r_vals.append(r)

    # Summarize the empirical distribution of correlations
    return pd.Series({
        "noise_ceiling_mean": np.nanmean(r_vals),
        "noise_ceiling_median": np.nanmedian(r_vals),
        "noise_ceiling_p05": np.nanpercentile(r_vals, 5),
        "noise_ceiling_p95": np.nanpercentile(r_vals, 95),
        "n_variants": len(sub),
    })

# ---------------------------------------------------------
# Run noise ceiling estimation for each gene
# ---------------------------------------------------------
results = []

for gene_id, sub in tqdm(df.groupby("gene_id"), desc="Processing genes"):
    res = compute_noise_ceiling_for_gene(sub)
    if res is not None:
        res["gene_id"] = gene_id
        results.append(res)

results_df = pd.DataFrame(results)

# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
results_df.to_csv(OUTPUT_FILE, index=False)

print(f"\n✔ Noise ceiling calculated and saved to {OUTPUT_FILE}")
