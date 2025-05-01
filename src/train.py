import os
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from src.data_utils import load_data, set_features
from src.model_utils import train_lightgbm
from src.evaluation import evaluate_predictions, collect_predictions
import src.config as config


def train():
    # Load and prepare data
    data = load_data(config.DATA_PATH)
    X = set_features(data, mode="drop")
    y = data["normalized_dms_score"]
    groups = data["gene_id"]

    # Train-test split
    splitter = GroupShuffleSplit(test_size=0.1, n_splits=1, random_state=42)
    train_idx, test_idx = next(splitter.split(X, y, groups=groups))
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    # Train model
    model = train_lightgbm(X_train, y_train, X_test, y_test)

    # Evaluate and collect metrics
    train_metrics = evaluate_predictions(y_train, model.predict(X_train))
    test_metrics = evaluate_predictions(y_test, model.predict(X_test))
    results = [collect_predictions(train_metrics, test_metrics, X_train, X_test)]

    # Save model
    model.save_model(config.MODEL_PATH)

    # Save evaluation results
    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(config.OUTPUT_DIR, "train_results.csv"), index=False)
