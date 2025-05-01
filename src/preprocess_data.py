from src.data_utils import fetch_data, preprocess
import src.config as config


def preprocess_data():
    data = fetch_data(config.QUERY_PATH, config.DB_URL)
    data.to_csv(config.RAW_DATA_PATH, index=False)
    data = preprocess(data)
    data.to_csv(config.PROCESSED_DATA_PATH, index=False)
