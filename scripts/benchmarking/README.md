## Benchmarking framework

To enable direct and reproducible comparison with existing deep mutational
scanning (DMS) imputation approaches, VEFill benchmarking adopts and extends
the framework introduced by Fu et al. (2023).

Specifically, the selection of the 146 DMS datasets and the 28 high-quality
datasets used for benchmarking, the implementations of the Residue-mean
baseline, Wu et al. (2019), Envision, FactorizeDMS, and AALasso, as well as
the overall benchmarking and visualization pipeline, were taken from and
adapted from the public repository accompanying that study:

https://github.com/PapenfussLab/Impute_DMS

The framework was extended to incorporate VEFill and additional baselines
(e.g. 5NN-based methods), to support cross-protein benchmarking under
realistic feature-availability constraints, and to enable evaluation under
varying training data completeness.