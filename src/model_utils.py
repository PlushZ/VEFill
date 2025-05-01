import json
import lightgbm as lgb
import src.config as config


def train_lightgbm(X_train, y_train, X_valid, y_valid, params=None):
    """Train LightGBM model with early stopping using predefined or custom parameters."""
    # Load default/best parameters if not provided
    if params is None:
        with open(config.BEST_PARAMS_PATH, "r") as f:
            params = json.load(f)

    # Add required LightGBM training parameters
    params.update(
        {
            "boosting_type": "gbdt",
            "objective": "regression",
            "metric": "rmse",
            "device": "gpu",
            "verbose": -1,
            "seed": 42,
        }
    )

    lgb_train = lgb.Dataset(X_train, label=y_train)
    lgb_valid = lgb.Dataset(X_valid, label=y_valid, reference=lgb_train)

    model = lgb.train(
        params,
        lgb_train,
        num_boost_round=1000,
        valid_sets=[lgb_train, lgb_valid],
        valid_names=["Train", "Test"],
        callbacks=[
            lgb.early_stopping(stopping_rounds=50, verbose=True),
            lgb.log_evaluation(period=100),
        ],
    )

    return model
