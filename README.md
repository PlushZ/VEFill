# VEFill: a model for accurate and generalizable deep mutation scanning score imputation across protein domains

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

The processed datasets used in this study, including both *Domainome* and *non-Domainome* data, are available via the [Zenodo repository](https://zenodo.org) in the `data/` directory. These datasets contain mutation-level features and target labels used to train and evaluate the models. They were generated using the preprocessing pipeline implemented in this repository (`src/preprocess_data.py`), which fetches raw data from a SQL database and applies transformations such as one-hot encoding, numerical standardization, and embedding flattening.

For demonstration purposes, we also provide a lightweight version of the *Domainome* dataset: `data/example_domainome_preprocessed.csv`. This example file contains a small but representative subset of the full dataset, including 3 distinct `gene_id` values, each with 3 unique `position`s, and 3 mutations per position (total of ~27 rows). It is useful for quickly inspecting the data structure or testing pipeline components without requiring the full heavy dataset.

### Restore the database

A PostgreSQL backup file of the used dataset is available at [Zenodo repository](https://zenodo.org) in the `db/` directory. It can be restored using `pg_restore` and includes all tables used to train VEFill.

To restore:

```bash
createdb vefill
pg_restore -U youruser -d vefill vefill_backup.dump
```

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Pretrained models

The following pretrained VEFill models are available at [Zenodo repository](https://zenodo.org) in the `models/` directory:

| Model type                | File location                                              |
|---------------------------|------------------------------------------------------------|
| General             | `models/lgbm_model.pkl`                                    |
| General (different feature sets) | `models/feature_sets/lgbm_model_{feature_set}.pkl`                                    |
| General LOPO (leave-one-protein-out) | `models/lopo_models/lgbm_model_excluding_gene_{gene_id}.pkl`         |
| Per-protein (random split)      | `models/per_protein_random_models/lgbm_model_{gene_id}.pkl`|
| Per-protein LPosO (stratified by position)      | `models/per_protein_lposo_models/lgbm_model_{gene_id}.pkl` |
| Per-protein LOPosO (leave-one-position-out)      | `models/per_protein_loposo_models/lgbm_model_gene_{gene_id}_excluding_pos_{position}.pkl` |
| Per-protein LOVarO (leave-one-variant-out)      | `models/per_protein_lovaro_models/lgbm_model_gene_{gene_id}_excluding_variant_{mutation_id}.pkl` |
| Reduced feature set (only ESM-1v embeddings and mean DMS used)     | `models/reduced/lgbm_model.pkl` |
| Zero-shot (without mean DMS)     | `models/zero_shot/lgbm_model.pkl` |
| Pretrained model from FAIR’s ESM-1v repo to generate ESM-1v embeddings for this study  | `models/esm_1v/esm1v_t33_650M_UR90S_1.pt` |

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

## License

MIT License. See `LICENSE` for details.