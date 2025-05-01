import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.train_per_protein_loposo import train_per_protein_loposo

if __name__ == "__main__":
    train_per_protein_loposo()
