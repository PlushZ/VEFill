import pandas as pd
import numpy as np
import json
from sqlalchemy import create_engine


def load_data(data_path: str) -> pd.DataFrame:
    return pd.read_csv(data_path)


def set_features(data: pd.DataFrame, mode: str = "drop") -> pd.DataFrame:
    if mode == "drop":
        features_to_drop = [
            "mutation_id",
            "position",
            "normalized_dms_score",
            "gene_id",
            "jse_normalized_dms",
            "eve_class_Uncertain",
            "eve_class_Pathogenic",
            "eve_class_Benign",
        ] + [
            col
            for col in data.columns
            if col.startswith(
                (
                    "alphafold_",
                    "alphamissense_",
                    "assay_",
                    "mutation_type_",
                    "diff_embedding_",
                )
            )
        ]
        return data.drop(columns=features_to_drop, errors="ignore")

    elif mode == "select":
        selected = ["mean_normalized_dms"] + [
            col
            for col in data.columns
            if col.startswith(
                ("wt_embedding_", "variant_embedding_", "diff_embedding_")
            )
        ]
        return data[selected]

    raise ValueError("Invalid mode. Use 'drop' or 'select'")


def fetch_data(query_path: str, db_url: str) -> pd.DataFrame:
    with open(query_path, "r") as file:
        query = file.read()
    engine = create_engine(db_url)
    with engine.connect() as conn:
        return pd.read_sql(query, conn)


def normalize_dms_scores(data: pd.DataFrame) -> pd.DataFrame:
    data["normalized_dms_score"] = (data["dms_score"] - data["wt_score"]) / (
        data["wt_score"] - data["non_score"]
    ) + 1
    return data


def compute_jse(scores: pd.Series) -> pd.Series:
    mu = scores.mean()
    var = scores.var(ddof=1)
    n = len(scores)
    if var == 0 or n <= 2:
        return pd.Series(mu, index=scores.index)
    shrink = max(0, 1 - (n - 2) * var / ((scores - mu) ** 2).sum())
    return pd.Series(mu + shrink * (scores - mu), index=scores.index)


def compute_mean_per_position(data: pd.DataFrame) -> pd.DataFrame:
    if not {"gene_id", "position", "normalized_dms_score"}.issubset(data.columns):
        raise ValueError("Missing columns for position-level aggregation")
    data["mean_normalized_dms"] = data.groupby(["gene_id", "position"])[
        "normalized_dms_score"
    ].transform("mean")
    return data


def flatten_embedding(embedding):
    if isinstance(embedding, str):
        try:
            embedding = json.loads(embedding)
        except json.JSONDecodeError:
            return pd.Series()
    if isinstance(embedding, (list, np.ndarray)):
        return pd.Series(
            embedding, index=[f"embedding_{i}" for i in range(len(embedding))]
        )
    return pd.Series(dtype="float64")


def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    # Normalize and compute score summaries
    data = normalize_dms_scores(data)
    data["jse_normalized_dms"] = data.groupby("gene_id")[
        "normalized_dms_score"
    ].transform(compute_jse)
    data = compute_mean_per_position(data)

    # One-hot encode categorical features
    cat_cols = [
        "assay_type",
        "eve_class_75_set",
        "alphafold_conf_type",
        "mutation_type",
    ]
    prefixes = {
        "assay_type": "assay",
        "eve_class_75_set": "eve_class",
        "alphafold_conf_type": "alphafold",
        "mutation_type": "mutation_type",
    }
    data = pd.get_dummies(data, columns=cat_cols, prefix=prefixes)

    # Encode amino acid categorical features
    for prop in ["chemical", "charge", "stabilizing_interaction", "volume"]:
        for prefix in ["wt", "variant"]:
            col = f"{prefix}_{prop}"
            if col in data.columns:
                data = pd.get_dummies(data, columns=[col], prefix=[col])

    # Encode boolean amino acid features and compute differences
    bool_props = [
        "h_bond_donor",
        "h_bond_acceptor",
        "solvent_accessible",
        "redox_reactivity",
        "amphipathic",
        "polar",
        "hydrophobic",
    ]
    for prop in bool_props:
        wt, var = f"wt_{prop}", f"variant_{prop}"
        if wt in data.columns and var in data.columns:
            data[wt] = data[wt].astype(int)
            data[var] = data[var].astype(int)
            data[f"{prop}_diff"] = abs(data[wt] - data[var])

    # Compute numeric property differences
    num_props = [
        "molecular_weight_da",
        "pka25_co2h",
        "pka25_nh2",
        "isoelectric_point_pl",
        "hydropathy_index",
    ]
    for prop in num_props:
        wt, var = f"wt_{prop}", f"variant_{prop}"
        if wt in data.columns and var in data.columns:
            data[f"{prop}_diff"] = abs(data[wt] - data[var])

    # Process edit_distance
    data["edit_distance"] = (
        pd.to_numeric(data.get("edit_distance", 0), errors="coerce")
        .fillna(0)
        .astype(int)
    )

    # Flatten and rename embedding columns
    for col, prefix in [
        ("embedding_wt", "wt_"),
        ("embedding_variant", "variant_"),
        ("embedding_difference", "diff_"),
    ]:
        if col in data.columns:
            flattened = data[col].apply(flatten_embedding)
            data = pd.concat([data, flattened.add_prefix(prefix)], axis=1)

    # Drop raw columns
    drop_cols = [
        "embedding_wt",
        "embedding_variant",
        "embedding_difference",
        "wt_residue",
        "variant_residue",
        "dms_score",
        "wt_score",
        "non_score",
    ]
    data = data.drop(columns=drop_cols, errors="ignore")

    # Coerce any remaining object/bool columns
    obj_cols = data.select_dtypes(include="object").columns
    data[obj_cols] = data[obj_cols].apply(
        lambda x: pd.to_numeric(x, errors="coerce").fillna(0).astype(int)
    )

    bool_cols = data.select_dtypes(include="bool").columns
    data[bool_cols] = data[bool_cols].astype(int)

    return data
