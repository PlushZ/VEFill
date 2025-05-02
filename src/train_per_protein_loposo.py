import os
import pandas as pd
from src.data_utils import load_data, set_features
from src.evaluation import (
    evaluate_predictions,
    collect_predictions,
    collect_mut_level_predictions,
)
from src.model_utils import train_lightgbm
import src.config as config


def train_per_protein_loposo():
    # Load and prepare data
    data = load_data(config.DATA_PATH)
    gene_ids = data["gene_id"].unique()

    # Set up directory for saving models
    model_dir = os.path.join(
        os.path.dirname(config.MODEL_PATH), "per_protein_loposo_models"
    )
    os.makedirs(model_dir, exist_ok=True)
    model_template = os.path.join(
        model_dir, "lgbm_model_gene_{gene_id}_excluding_pos_{position}.pkl"
    )

    for gene_id in gene_ids:
        gene_data = data[data["gene_id"] == gene_id]
        unique_positions = gene_data["position"].unique()

        # Skip genes with too few positions
        if len(unique_positions) < 2:
            continue

        position_results = []
        performance_results = []

        # Leave-one-position-out per gene
        for position_out in unique_positions:
            train_data = gene_data[gene_data["position"] != position_out]
            test_data = gene_data[gene_data["position"] == position_out]

            if train_data.empty or test_data.empty:
                continue

            # Extract features and targets
            X_train = set_features(train_data, mode="drop")
            y_train = train_data["normalized_dms_score"]
            X_test = set_features(test_data, mode="drop")
            y_test = test_data["normalized_dms_score"]

            # Train model
            model = train_lightgbm(X_train, y_train, X_test, y_test)

            # Evaluate and collect metrics
            y_pred_test = model.predict(X_test, num_iteration=model.best_iteration)
            train_metrics = evaluate_predictions(y_train, model.predict(X_train))
            test_metrics = evaluate_predictions(y_test, y_pred_test)

            # Collect mutation-level and performance results
            position_results.extend(
                collect_mut_level_predictions(
                    y_test,
                    y_pred_test,
                    test_data["mutation_id"],
                    position_out,
                    gene_id=gene_id,
                )
            )
            performance_results.append(
                collect_predictions(
                    train_metrics,
                    test_metrics,
                    X_train,
                    X_test,
                    gene_id=gene_id,
                    position_out=position_out,
                )
            )

            # Save model
            model_path = model_template.format(gene_id=gene_id, position=position_out)
            model.save_model(model_path)

        # Save per-gene results
        pd.DataFrame(position_results).to_csv(
            os.path.join(config.OUTPUT_DIR, f"loposo_positions_gene_{gene_id}.csv"),
            index=False,
        )
        pd.DataFrame(performance_results).to_csv(
            os.path.join(config.OUTPUT_DIR, f"loposo_performance_gene_{gene_id}.csv"),
            index=False,
        )
