import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocess_data import preprocess_data

if __name__ == "__main__":
    preprocess_data()
