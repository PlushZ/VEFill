import os
import numpy as np
import pandas as pd
import lightgbm as lgb
from src.data_utils import set_features
from src.evaluation import evaluate_predictions
import src.config as config


def inference():
    # Load input data and pretrained model
    data = pd.read_csv(config.INFERENCE_DATA_PATH)
    model = lgb.Booster(model_file=config.MODEL_PATH)

    X = set_features(data, mode="drop")
    y = data["normalized_dms_score"]

    for gene_id in data["gene_id"].unique():
        gene_mask = data["gene_id"] == gene_id
        gene_X = X.loc[gene_mask]
        gene_y = y.loc[gene_mask]

        # Apply random masking
        np.random.seed(42)
        mask = np.random.rand(len(gene_y)) < config.MASK_RATIO
        if mask.sum() == 0:
            continue

        X_masked = gene_X[mask]
        y_true = gene_y[mask]
        y_pred = model.predict(X_masked)

        # Save predictions
        results_df = pd.DataFrame(
            {
                "gene_id": gene_id,
                "mutation_id": data.loc[gene_mask, "mutation_id"][mask].values,
                "position": data.loc[gene_mask, "position"][mask].values,
                "y_true": y_true.values,
                "y_pred": y_pred,
                "absolute_error": np.abs(y_true - y_pred),
                "squared_error": (y_true - y_pred) ** 2,
                "percentage_error": np.abs(y_true - y_pred) / np.abs(y_true) * 100,
            }
        )

        pred_path = os.path.join(
            config.OUTPUT_DIR, f"inference_predictions_gene_{gene_id}.csv"
        )
        results_df.to_csv(pred_path, index=False)

        # Save metrics
        metrics = evaluate_predictions(y_true, y_pred)
        metrics_df = pd.DataFrame(
            [{"gene_id": gene_id, "n_mutations": len(y_true), **metrics}]
        )

        metrics_path = os.path.join(
            config.OUTPUT_DIR, f"inference_metrics_gene_{gene_id}.csv"
        )
        metrics_df.to_csv(metrics_path, index=False)
