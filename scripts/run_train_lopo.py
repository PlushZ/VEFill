import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.train_lopo import train_lopo

if __name__ == "__main__":
    train_lopo()
