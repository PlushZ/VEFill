import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.inference import inference

if __name__ == "__main__":
    inference()
