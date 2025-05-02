import os
import pandas as pd
from src.data_utils import load_data, set_features
from src.evaluation import (
    evaluate_predictions,
    collect_mut_level_predictions,
    collect_predictions,
)
from src.model_utils import train_lightgbm
import src.config as config


def train_per_protein_lovaro():
    # Load and prepare data
    data = load_data(config.DATA_PATH)
    gene_ids = data["gene_id"].unique()

    # Set up directory for saving models
    model_dir = os.path.join(
        os.path.dirname(config.MODEL_PATH), "per_protein_lovaro_models"
    )
    os.makedirs(model_dir, exist_ok=True)
    model_template = os.path.join(
        model_dir, "lgbm_model_gene_{gene_id}_excluding_variant_{mutation_id}.pkl"
    )

    for gene_id in gene_ids:
        gene_data = data[data["gene_id"] == gene_id]
        variants = gene_data["mutation_id"].unique()

        # Skip genes with too few variants
        if len(variants) < 2:
            continue

        mutation_results = []
        performance_results = []

        # Leave-one-variant-out per gene
        for variant_out in variants:
            train_data = gene_data[gene_data["mutation_id"] != variant_out]
            test_data = gene_data[gene_data["mutation_id"] == variant_out]

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
            mutation_results.extend(
                collect_mut_level_predictions(
                    y_test,
                    y_pred_test,
                    test_data["mutation_id"],
                    variant_out=variant_out,
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
                    variant_out=variant_out,
                )
            )

            # Save model
            model_path = model_template.format(gene_id=gene_id, mutation_id=variant_out)
            model.save_model(model_path)

        # Save prediction and performance results per gene
        pd.DataFrame(mutation_results).to_csv(
            os.path.join(config.OUTPUT_DIR, f"lovaro_variants_gene_{gene_id}.csv"),
            index=False,
        )
        pd.DataFrame(performance_results).to_csv(
            os.path.join(config.OUTPUT_DIR, f"lovaro_performance_gene_{gene_id}.csv"),
            index=False,
        )
