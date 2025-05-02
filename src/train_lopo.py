import os
import pandas as pd
from src.data_utils import load_data, set_features
from src.evaluation import evaluate_predictions, collect_predictions
from src.model_utils import train_lightgbm
import src.config as config


def train_lopo():
    # Load and prepare data
    data = load_data(config.DATA_PATH)
    X = set_features(data, mode="drop")
    y = data["normalized_dms_score"]
    gene_ids = data["gene_id"]
    unique_gene_ids = gene_ids.unique()

    # Initialize results container
    results = []

    # Set up directory for saving models
    model_dir = os.path.join(os.path.dirname(config.MODEL_PATH), "lopo_models")
    os.makedirs(model_dir, exist_ok=True)
    model_template = os.path.join(model_dir, "lgbm_model_excluding_gene_{gene_id}.pkl")

    for gene_id_out in unique_gene_ids:
        train_mask = gene_ids != gene_id_out
        test_mask = gene_ids == gene_id_out

        if test_mask.sum() == 0:
            continue

        X_train, y_train = X.loc[train_mask], y.loc[train_mask]
        X_test, y_test = X.loc[test_mask], y.loc[test_mask]

        # Train model
        model = train_lightgbm(X_train, y_train, X_test, y_test)

        # Evaluate and collect metrics
        train_metrics = evaluate_predictions(y_train, model.predict(X_train))
        test_metrics = evaluate_predictions(y_test, model.predict(X_test))

        results.append(
            collect_predictions(
                train_metrics, test_metrics, X_train, X_test, gene_id_out=gene_id_out
            )
        )

        # Save model
        model_path = model_template.format(gene_id=gene_id_out)
        model.save_model(model_path)

    # Save evaluation results
    results_df = pd.DataFrame(results)
    results_path = os.path.join(config.OUTPUT_DIR, "lopo_results.csv")
    results_df.to_csv(results_path, index=False)
