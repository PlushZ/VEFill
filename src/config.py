import os
from decouple import config as env_config

# Environment variables
DB_URL = env_config("DB_URL", default=None)
if not DB_URL:
    raise ValueError("Environment variable DB_URL is not set.")

# File paths
QUERY_PATH = "data/queries/extract_data.sql"

RAW_DATA_PATH = "data/raw/domainome.csv"
PROCESSED_DATA_PATH = "data/domainome_preprocessed.csv"
DATA_PATH = PROCESSED_DATA_PATH
INFERENCE_DATA_PATH = "data/non_domainome_preprocessed.csv"

MODEL_PATH = "models/lgbm_model.pkl"
BEST_PARAMS_PATH = "models/best_params.json"
OUTPUT_DIR = "results/"

# Parameters
MASK_RATIO = 0.3

# Ensure required directories exist
for path in [
    QUERY_PATH,
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    DATA_PATH,
    INFERENCE_DATA_PATH,
    MODEL_PATH,
    BEST_PARAMS_PATH,
]:
    os.makedirs(os.path.dirname(path), exist_ok=True)

os.makedirs(OUTPUT_DIR, exist_ok=True)
