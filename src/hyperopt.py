import json
import optuna
import lightgbm as lgb
from sklearn.model_selection import GroupKFold, GroupShuffleSplit, cross_val_score
from src.data_utils import load_data, set_features
import src.config as config


def hyperopt():
    # Load and prepare data
    data = load_data(config.DATA_PATH)
    X = set_features(data, mode="drop")
    y = data["normalized_dms_score"]
    groups = data["gene_id"]

    # Train-test split
    train_idx, _ = next(
        GroupShuffleSplit(test_size=0.1, n_splits=1, random_state=42).split(
            X, y, groups
        )
    )
    X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
    train_groups = groups.iloc[train_idx]

    # Objective function for Optuna
    def objective(trial):
        params = {
            "boosting_type": "gbdt",
            "objective": "regression",
            "metric": "rmse",
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
            "max_depth": trial.suggest_int("max_depth", -1, 16),
            "num_leaves": trial.suggest_int("num_leaves", 31, 128),
            "min_child_samples": trial.suggest_int("min_child_samples", 10, 50),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
            "device": "gpu",
            "verbose": -1,
            "seed": 42,
        }
        cv = GroupKFold(n_splits=5)
        scores = cross_val_score(
            lgb.LGBMRegressor(**params),
            X_train,
            y_train,
            groups=train_groups,
            cv=cv,
            scoring="neg_root_mean_squared_error",
        )
        return -scores.mean()

    # Run optimization
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=50, timeout=3600)

    # Save best parameters
    with open(config.BEST_PARAMS_PATH, "w") as f:
        json.dump(study.best_params, f)
