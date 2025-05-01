# VEFill: a model for accurate and generalizable deep mutation scanning score imputation across protein domains

This repository contains code, data processing scripts, and training routines for predicting deep mutational scanning (DMS) scores from variant features using LightGBM-based regression model.

---

## Directory Structure

| Folder/File         | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `data/`             | SQL queries, raw and processed datasets                                     |
| `db/`               | Scripts for populating a local database with mutation features              |
| `models/`           | Pretrained LightGBM models (see table below)                                |
| `results/`          | Model output files (metrics, predictions)                                   |
| `scripts/`          | Entry-point run scripts for preprocessing, training, inference              |
| `src/`              | Source code: preprocessing, training, evaluation, configuration             |

---

## Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Pretrained Models

The following pretrained models are available in the `models/` directory:

| Model type                | File location                                              |
|---------------------------|------------------------------------------------------------|
| General             | `models/lgbm_model.pkl`                                    |
| General (different feature sets) | `models/feature_sets/`                                    |
| General LOPO (leave-one-protein-out) | `models/lopo_models/lgbm_model_gene_{gene_id}.pkl`         |
| Per-protein (random split)      | `models/per_protein_random_models/lgbm_model_{gene_id}.pkl`|
| Per-protein LPosO (stratified by position)      | `models/per_protein_lposo_models/lgbm_model_{gene_id}.pkl` |
| Per-protein LOPosO (leave-one-position-out)      | `models/per_protein_loposo_models/lgbm_model_gene_{gene_id}_pos_{position}.pkl` |
| Per-protein LOVarO (leave-one-variant-out)      | `models/per_protein_lovaro_models/lgbm_model_gene_{gene_id}_variant_{mutation_id}.pkl` |
| Zero-shot (only ESM-1v embeddings and mean DMS used)     | `models/per_protein_lovaro_models/lgbm_model_gene_{gene_id}_variant_{mutation_id}.pkl` |

---

## Data Access

The processed datasets used in this study, including both *Domainome* and *non-Domainome* variant data, are available via the [Zenodo repository](https://zenodo.org). These datasets contain mutation-level features and target labels used to train and evaluate the models. All data was generated using the preprocessing pipeline included in this repository.

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