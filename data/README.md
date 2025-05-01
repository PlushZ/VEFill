# Data Overview

This directory contains or references the datasets used for training and evaluating VEFill.

## Available Datasets

The following preprocessed datasets are provided:

- **Domainome dataset**: Includes data from _Human Domainome 1_ 
- **Non-Domainome dataset**: Includes data from other proteins

Each dataset includes mutation-level features and corresponding normalized DMS scores, ready for use in model training.

## Download Location

The processed datasets are available at:

[Zenodo Repository](https://zenodo.org)

They were generated using the preprocessing pipeline implemented in this repository (`src/preprocess_data.py`), which fetches raw data from a SQL database and applies transformations such as one-hot encoding, numerical standardization, and embedding flattening.
