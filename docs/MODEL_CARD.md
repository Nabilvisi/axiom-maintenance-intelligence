# Axiom — Model Card

Model: axiom-rf-v1 · Seed: 42 · Release: 8 October 2026

## Intended use

Portfolio demonstration of operating-state failure classification, probability calibration and hypothetical inspection-policy analysis. Not approved for controlling industrial equipment, forecasting remaining useful life, predicting failure within a future window, or autonomous maintenance decisions.

## Dataset

AI4I 2020, UCI, synthetic, 10,000 observations, 339 positive labels. License CC BY 4.0. Source: https://doi.org/10.24432/C5HS5C.

Dataset SHA-256: `dc6630cd9b1f0f853922fad78a1b6436570d3f1ec863f1dd5c4340ac56bc8a8e`.

## Evaluation

Train 6,000; calibration 2,000; test 2,000. Stratified random split; 68 test failures. IDs and all failure-mode labels excluded. Derived features are temperature delta, mechanical power and wear × torque.

| Model | AP | AUROC | Brier |
|---|---:|---:|---:|
| Calibrated logistic baseline | 0.358896 | 0.923643 | 0.025715 |
| Calibrated random forest | 0.849204 | 0.984997 | 0.008563 |

Forest AP bootstrap 95% interval: 0.758248–0.924568, 400 fixed-seed resamples. This describes holdout resampling variability, not field transfer uncertainty.

Separate contiguous-row stress test: AP 0.700596, AUROC 0.919945, Brier 0.007611; 39 positive labels among the final 2,000 rows. This uses row order as a proxy because actual timestamps and machine identities are unavailable. The lower AP demonstrates evaluation-design sensitivity.

## Default decision policy

Calibration-set cost-selected threshold 0.005 (0.5%). Test confusion counts: TP 66, FP 148, TN 1784, FN 2. Inspections 214/2,000; recall 0.970588; precision 0.308411.

Assumed inspection $150 and missed-failure $12,000. Hypothetical policy cost $56,100; no-inspection baseline $816,000. Inspection is assumed to prevent loss perfectly on an inspected failed observation. Neither costs nor savings are real measurements.

Calibration and threshold choice share a calibration split, so policy-selection optimism remains possible. Interactive adjustments on test data are exploratory and cannot be claimed as unbiased policy performance.

## Subgroup evidence

| Quality type | Observations | Failures | AP | Recall |
|---|---:|---:|---:|---:|
| L | 1179 | 41 | 0.894306 | 1.000000 |
| M | 623 | 24 | 0.818756 | 0.916667 |
| H | 198 | 3 | 0.609524 | 1.000000 |

H has only three test failures. High point-estimate recall does not establish robust subgroup performance. Quality categories are not demographic groups; no demographic fairness assessment is possible here.

## Explanation

Feature sensitivity replaces one numeric sensor at a time with its training median, recomputes engineered features and subtracts the new score from the original. This is nonadditive, noncausal, and not SHAP. Correlated sensors can make replacement states unrealistic.

## Known limitations

- Synthetic, partly rule-generated labels; strong benchmark results do not establish industrial capability.
- Recorded-state classification, no lead time or future prediction horizon.
- Random-split dependence and absent machine-level grouping.
- Small positive subgroups and random failure components.
- Calibration/prevalence shift outside the benchmark population.
- No tested maintenance efficacy, alert capacity, live drift monitoring or realized business value.
- UI ranges permit some out-of-support inputs; range warnings are not guarantees of safe extrapolation.

## Runtime and verification

Exported forest with float32 inputs and isotonic interpolation. Thirty full-precision parity fixtures and all 2,000 rounded display predictions match Python at the defined tolerances. Input validation, body limits, split disjointness and policy counts are checked.

## Before production use

Obtain dated per-equipment sensor histories and a forecast target. Conduct grouped temporal backtests, separate policy validation, prevalence-aware recalibration, realistic cost/efficacy studies, a supervised pilot, monitoring with delayed outcomes, load/security review, and rollback planning.
