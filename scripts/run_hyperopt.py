import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.hyperopt import hyperopt

if __name__ == "__main__":
    hyperopt()
