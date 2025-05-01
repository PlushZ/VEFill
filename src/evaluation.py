from math import sqrt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import pearsonr
import numpy as np


def evaluate_predictions(y_true, y_pred):
    """Compute standard regression metrics."""
    rmse = sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    r = pearsonr(y_true, y_pred)[0] if len(y_true) > 1 else np.nan

    return {"RMSE": rmse, "MAE": mae, "R2": r2, "r": r}


def collect_predictions(
    train_metrics,
    test_metrics,
    X_train,
    X_test,
    gene_id=None,
    gene_id_out=None,
    position_out=None,
    variant_out=None,
):
    """Collect model performance summary for train and test splits."""
    result = {
        "train_size": X_train.shape[0],
        "train_RMSE": train_metrics["RMSE"],
        "train_MAE": train_metrics["MAE"],
        "train_R2": train_metrics["R2"],
        "train_r": train_metrics["r"],
        "test_size": X_test.shape[0],
        "test_RMSE": test_metrics["RMSE"],
        "test_MAE": test_metrics["MAE"],
        "test_R2": test_metrics["R2"],
        "test_r": test_metrics["r"],
    }
    if gene_id is not None:
        result["gene_id"] = gene_id
    if gene_id_out is not None:
        result["gene_id_out"] = gene_id_out
    if position_out is not None:
        result["position_out"] = position_out
    if variant_out is not None:
        result["variant_out"] = variant_out
    return result


def collect_mut_level_predictions(
    y_true, y_pred, ids, position_out=None, variant_out=None, gene_id=None
):
    """Collect mutation-level prediction results with error metrics."""
    results = []
    for i in range(len(y_true)):
        true_val = y_true.iloc[i]
        pred_val = y_pred[i]
        mutation_id = ids.iloc[i]
        error = abs(true_val - pred_val)
        squared_error = error**2
        percentage_error = (
            (error / abs(true_val)) * 100 if true_val != 0 else float("inf")
        )

        result = {
            "mutation_id": mutation_id,
            "y_true": true_val,
            "y_pred": pred_val,
            "absolute_error": error,
            "squared_error": squared_error,
            "percentage_error": percentage_error,
        }
        if gene_id is not None:
            result["gene_id"] = gene_id
        if position_out is not None:
            result["position_out"] = position_out
        if variant_out is not None:
            result["variant_out"] = variant_out

        results.append(result)
    return results
