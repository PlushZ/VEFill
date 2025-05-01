import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.data_utils import load_data, set_features
from src.evaluation import evaluate_predictions, collect_predictions
from src.model_utils import train_lightgbm
import src.config as config


def train_per_protein_lposo():
    # Load and prepare data
    data = load_data(config.DATA_PATH)
    gene_ids = data["gene_id"].unique()
    results = []

    # Set up directory for saving models
    model_dir = os.path.join(
        os.path.dirname(config.MODEL_PATH), "per_protein_lposo_models"
    )
    os.makedirs(model_dir, exist_ok=True)
    model_template = os.path.join(model_dir, "lgbm_model_{gene_id}.pkl")

    for gene_id in gene_ids:
        gene_data = data[data["gene_id"] == gene_id]

        # Stratified split by position
        unique_positions = gene_data["position"].unique()
        if len(unique_positions) < 2:
            continue

        test_size = 0.2 if len(unique_positions) > 5 else 1 / len(unique_positions)
        train_pos, test_pos = train_test_split(
            unique_positions, test_size=test_size, random_state=42
        )
        train_data = gene_data[gene_data["position"].isin(train_pos)]
        test_data = gene_data[gene_data["position"].isin(test_pos)]

        if train_data.empty or test_data.empty:
            continue

        # Extract features and targets
        X_train = set_features(train_data, mode="drop")
        X_test = set_features(test_data, mode="drop")
        y_train = train_data["normalized_dms_score"]
        y_test = test_data["normalized_dms_score"]

        # Train model
        model = train_lightgbm(X_train, y_train, X_test, y_test)

        # Evaluate and collect metrics
        train_metrics = evaluate_predictions(y_train, model.predict(X_train))
        test_metrics = evaluate_predictions(y_test, model.predict(X_test))

        results.append(
            collect_predictions(
                train_metrics, test_metrics, X_train, X_test, gene_id=gene_id
            )
        )

        # Save model
        model_path = model_template.format(gene_id=gene_id)
        model.save_model(model_path)

    # Save results
    results_df = pd.DataFrame(results)
    results_path = os.path.join(config.OUTPUT_DIR, "per_protein_lposo_results.csv")
    results_df.to_csv(results_path, index=False)
