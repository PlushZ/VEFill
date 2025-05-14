# VEFill: a model for accurate and generalizable deep mutational scanning score imputation across protein domains

This repository contains code, data processing scripts, and training routines for predicting deep mutational scanning (DMS) scores from variant features using LightGBM-based regression model.

---

## Directory structure

| Folder              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `data/`             | SQL queries, and example of processed dataset                               |
| └─ `queries/`       | SQL for data extraction                                                     |
| `db/`               | Scripts and modules for database schema, ORM, and population                |
| └─ `orm/`           | SQLAlchemy models and DB session handling                                   |
| └─ `schema/`        | SQL schema definitions                                                      |
| └─ `scripts/`       | Scripts to populate DB with computed embeddings                             |
| `models/`           | Pretrained LightGBM model and best hyperparameters                          |
| `results/`          | Model outputs: predictions and evaluation metrics                           |
| `scripts/`          | Entry-point scripts for running preprocessing, training, and inference      |
| `src/`              | Core logic: training, preprocessing, model utils, evaluation modules        |

---

## Data access

The processed datasets used in this study, including both *Domainome* and *non-Domainome* data, are available via the Zenodo repository [10.5281/zenodo.15329750](https://doi.org/10.5281/zenodo.15329750) in the `data/` directory. These datasets contain mutation-level features and target labels used to train and evaluate the models. They were generated using the preprocessing pipeline implemented in this repository (`src/preprocess_data.py`), which fetches raw data from a SQL database and applies transformations such as one-hot encoding, numerical standardization, and embedding flattening.

For demonstration purposes, we also provide a lightweight version of the *Domainome* dataset: `data/example_domainome_preprocessed.csv`. This example file contains a small but representative subset of the full dataset, including 3 distinct `gene_id` values, each with 3 unique `position`s, and 3 mutations per position (total of ~27 rows). It is useful for quickly inspecting the data structure or testing pipeline components without requiring the full heavy dataset.

### Restore the database

A PostgreSQL backup file of the used dataset is available at [10.5281/zenodo.15329750](https://doi.org/10.5281/zenodo.15329750) in the `db/` directory. It can be restored using `pg_restore` and includes all tables used to train VEFill.

To restore:

```bash
createdb vefill
pg_restore -U youruser -d vefill vefill_backup.dump
```

---

## Installation

This project supports two ways to install dependencies: using **Poetry** (recommended) or using `pip` with a `requirements.txt`.

### Option 1: Using Poetry (recommended)

Poetry ensures a consistent environment using a lockfile.

1. Install Poetry (https://python-poetry.org/docs/#installation):  
   ```bash
   pip install poetry
   ```
2. Create the environment to install dependencies (**without** installing the project as a package):
   ```bash
   poetry install --no-root
   ```
3. Activate the virtual environment:
   ```bash
   source $(poetry env info --path)/bin/activate
   ```

### Option 2: Using pip and requirements.txt

If you prefer a traditional `pip` setup:

Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

---

## Reproducibility

To rerun the full pipeline:

1. **Preprocess data:**
   ```bash
   python scripts/run_preprocess_data.py
   ```

2. **Optimize hyperparameters:**
   ```bash
   python scripts/run_hyperopt.py
   ```

3. **Train model (general):**
   ```bash
   python scripts/run_train.py
   ```

4. **Perform inference:**
   ```bash
   python scripts/run_inference.py
   ```

---

## Pretrained models

The following pretrained VEFill models are available at [10.5281/zenodo.15329750](https://doi.org/10.5281/zenodo.15329750) in the `models/` directory:

| Model type                | File location                                              |
|---------------------------|------------------------------------------------------------|
| General             | `models/lgbm_model.pkl`                                    |
| General (different feature sets) | `models/feature_sets/lgbm_model_{feature_set}.pkl`                                    |
| General LOPO (leave-one-protein-out) | `models/lopo_models/lgbm_model_excluding_gene_{gene_id}.pkl`         |
| Per-protein (random split)      | `models/per_protein/random_split/lgbm_model_{gene_id}.pkl`|
| Per-protein LPosO (stratified by position)      | `models/per_protein/lposo/lgbm_model_{gene_id}.pkl` |
| Per-protein LOPosO (leave-one-position-out)      | `models/per_protein/loposo/lgbm_model_gene_{gene_id}_excluding_pos_{position}.pkl` |
| Per-protein LOVarO (leave-one-variant-out)      | `models/per_protein/lovaro/lgbm_model_gene_{gene_id}_excluding_variant_{mutation_id}.pkl` |
| Per-protein Split by SNV      | `models/per_protein/snv_split/lgbm_model_gene_{gene_id}_lnsnvo.pkl` |
| Reduced feature set (only ESM-1v embeddings and mean DMS used)     | `models/reduced/lgbm_model.pkl` |
| Zero-shot (without mean DMS)     | `models/zero_shot/lgbm_model.pkl` |

---

## License

MIT License. See `LICENSE` for details.