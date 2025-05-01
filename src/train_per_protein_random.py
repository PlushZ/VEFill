import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.data_utils import load_data, set_features
from src.evaluation import evaluate_predictions, collect_predictions
from src.model_utils import train_lightgbm
import src.config as config


def train_per_protein_random():
    # Load and prepare data
    data = load_data(config.DATA_PATH)
    gene_ids = data["gene_id"].unique()

    results = []

    # Set up directory for saving models
    model_dir = os.path.join(
        os.path.dirname(config.MODEL_PATH), "per_protein_random_models"
    )
    os.makedirs(model_dir, exist_ok=True)
    model_template = os.path.join(model_dir, "lgbm_model_{gene_id}.pkl")

    for gene_id in gene_ids:
        gene_data = data[data["gene_id"] == gene_id]

        if gene_data.shape[0] < 2:
            continue

        # Extract features and targets
        X = set_features(gene_data, mode="drop")
        y = gene_data["normalized_dms_score"]

        # Random 80/20 train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        if X_train.empty or X_test.empty:
            continue

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

    # Save metrics for all models
    results_df = pd.DataFrame(results)
    results_path = os.path.join(config.OUTPUT_DIR, "per_protein_random_results.csv")
    results_df.to_csv(results_path, index=False)
