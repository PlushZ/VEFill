"""
dms_completeness.py

Compute dataset-level variant completeness for Deep Mutational Scanning (DMS)
experiments from a local MaveDB CSV dump.

Definition of completeness:
    completeness = (number of reported variant scores) /
                   (number of scanned residues × 20)

This definition assumes that, for each scanned residue, all 20 possible
amino-acid substitutions are in principle observable.

Output:
- One row per dataset (CSV file)
- Includes total scanned residues, number of reported variants,
  raw completeness value, and a binned completeness category
"""

import os
import re
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
# Folder containing per-assay MaveDB CSV files
FOLDER = "data/mavedb-dump-zenodo/"

# Output summary file
OUTPUT_FILE = "results/completeness/mavedb_completeness_summary.csv"

# ---------------------------------------------------------
# Helper: extract numeric residue position from HGVS protein notation
# ---------------------------------------------------------
# Example: "p.Gly12Asp" → 12
def extract_position(hgvs_pro):
    """
    Extract the first numeric residue position from an HGVS protein string.

    Returns:
        int or NaN if no numeric position is found.
    """
    match = re.findall(r"\d+", str(hgvs_pro))
    if match:
        return int(match[0])
    return np.nan

# ---------------------------------------------------------
# Helper: assign completeness bin
# ---------------------------------------------------------
# Completeness bins are defined to match manuscript figures
# and summary tables.
def completeness_bin(c):
    """
    Assign a categorical completeness bin based on the raw completeness value.
    """
    if c > 1:
        return "c > 1"
    if c == 1:
        return "1"
    if c < 0.1:
        return "0 < c < 0.1"
    if c < 0.2:
        return "0.1 ≤ c < 0.2"
    if c < 0.3:
        return "0.2 ≤ c < 0.3"
    if c < 0.4:
        return "0.3 ≤ c < 0.4"
    if c < 0.5:
        return "0.4 ≤ c < 0.5"
    if c < 0.6:
        return "0.5 ≤ c < 0.6"
    if c < 0.7:
        return "0.6 ≤ c < 0.7"
    if c < 0.8:
        return "0.7 ≤ c < 0.8"
    if c < 0.9:
        return "0.8 ≤ c < 0.9"
    if c < 1:
        return "0.9 ≤ c < 1"
    return "Unknown"

# ---------------------------------------------------------
# Main processing loop
# ---------------------------------------------------------
# Identify all CSV files in the input folder
files = [f for f in os.listdir(FOLDER) if f.endswith(".csv")]

results = []

for file in files:
    filepath = os.path.join(FOLDER, file)

    # Load dataset
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"❌ Error reading {file}: {e}")
        continue

    # Validate required columns
    if "hgvs_pro" not in df.columns or "score" not in df.columns:
        print(f"⚠️ Skipping {file}: missing hgvs_pro or score columns.")
        continue

    # Extract numeric residue positions
    df["position"] = df["hgvs_pro"].apply(extract_position)
    df = df.dropna(subset=["position"])

    if df.empty:
        print(f"⚠️ Skipping {file}: no valid mutation rows after parsing.")
        continue

    # Identify scanned residue positions
    scanned_positions = df["position"].unique()
    n_scanned = len(scanned_positions)

    # Identify variants with reported scores
    df["reported"] = df["score"].notna() & (df["score"] != "")
    n_reported = int(df["reported"].sum())

    # Compute completeness
    completeness = n_reported / (n_scanned * 20)

    # Store summary statistics
    results.append({
        "selected_file": file,
        "scanned_residues": n_scanned,
        "reported_variants": n_reported,
        "completeness": completeness,
        "completeness_group": completeness_bin(completeness),
    })

# ---------------------------------------------------------
# Save summary table
# ---------------------------------------------------------
results_df = pd.DataFrame(results)
results_df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Saved completeness summary to: {OUTPUT_FILE}")
print(f"Processed {len(results_df)} valid files.")
