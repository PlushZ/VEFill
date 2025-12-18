import os
import json
import pandas as pd
import lightgbm as lgb
from src.data_utils import load_data, set_features
from src.evaluation import evaluate_predictions, collect_predictions
import src.config as config


def train_per_protein_substitution_classes():
    # Allowed amino-acid substitution classes
    allowed_variants = {"H", "E", "N", "I", "G"}

    # Load data
    data = load_data(config.DATA_PATH_DOMAINOME)

    if "variant_residue" not in data.columns:
        raise ValueError("Dataset must contain column 'variant_residue'")

    gene_ids = data["gene_id"].unique()

    # Load tuned LightGBM parameters
    with open(config.BEST_PARAMS_PATH, "r") as f:
        best_params = json.load(f)

    best_params.update(
        {
            "boosting_type": "gbdt",
            "objective": "regression",
            "metric": "rmse",
            "device": "gpu",
            "verbose": -1,
            "seed": 42,
        }
    )

    # Set up directory for saving models
    model_dir = os.path.join(
        os.path.dirname(config.MODEL_PATH), "aa_class_models"
    )
    os.makedirs(model_dir, exist_ok=True)
    model_template = os.path.join(
        model_dir, "lgbm_model_gene_{gene_id}_aa-classes.pkl"
    )

    results = []

    for gene_id in gene_ids:
        gene_data = data[data["gene_id"] == gene_id]

        train_data = gene_data[
            gene_data["variant_residue"].isin(allowed_variants)
        ]
        test_data = gene_data[
            ~gene_data["variant_residue"].isin(allowed_variants)
        ]

        if train_data.empty or test_data.empty:
            continue

        # Extract features and targets
        X_train = set_features(train_data, mode="drop")
        y_train = train_data["normalized_dms_score"]
        X_test = set_features(test_data, mode="drop")
        y_test = test_data["normalized_dms_score"]

        # Train model
        lgb_train = lgb.Dataset(X_train, label=y_train)
        lgb_valid = lgb.Dataset(X_test, label=y_test, reference=lgb_train)

        model = lgb.train(
            best_params,
            lgb_train,
            num_boost_round=1000,
            valid_sets=[lgb_train, lgb_valid],
            valid_names=["Train", "Test"],
            callbacks=[
                lgb.early_stopping(stopping_rounds=50, verbose=False),
                lgb.log_evaluation(period=0),
            ],
        )

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
    results_path = os.path.join(
        config.OUTPUT_DIR, "aa_substitution_class_results.csv"
    )
    results_df.to_csv(results_path, index=False)