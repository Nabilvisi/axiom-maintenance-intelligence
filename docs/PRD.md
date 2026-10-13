# Axiom — Product Requirements Document

Version 1.0 · Owner: Nabil Visi Samawi · 8 October 2026

## 1. Product and business problem

Axiom is a predictive-maintenance decision-support portfolio product. Its core question is: **Which operating observations should be inspected, and what evidence supports that decision?**

A high classification score alone does not answer that question. A useful product must explain its data provenance, expose the workload-versus-missed-failure trade-off, distinguish assumptions from results, and let a reviewer challenge the evaluation.

This implementation uses the UCI AI4I 2020 synthetic benchmark. It is a functioning analytical product, not live machine monitoring. A row is an operating observation; a product identifier is not established as a persistent machine identity. The target is the recorded state’s failure label, not a future time-horizon prediction.

## 2. Intended users

| User | Need | Main workflow |
|---|---|---|
| Reliability analyst | Prioritize attention and understand a risky state | Filter scope → inspect queue → review sensors and sensitivity |
| Operations decision maker | Compare workload and assumed losses | Change threshold and costs → compare confusion counts and scenario cost |
| Data science reviewer | Verify evaluation and limitations | Compare baseline, calibration, slices, ordered stress test, artifacts |
| Portfolio assessor | Understand the complete delivery | Read PRD/TRD/UIRD, run pipeline, inspect API and reproducibility checks |

## 3. Goals

1. Deliver a coherent, usable website with server inference and reproducible model training.
2. Connect calibrated model outputs to an explicit inspection policy.
3. Use 3D as a data exploration tool, with a usable table alternative.
4. Publish complete requirements and model provenance alongside the interface.
5. Demonstrate senior engineering judgment without claiming real production impact or years of experience.

## 4. Scope shipped in v1

- Frozen 2,000-observation test snapshot from a 10,000-row benchmark.
- L/M/H product quality filtering.
- Interactive 3D operating-space scatter: wear, torque, and rotational speed.
- Point selection, camera orbit, zoom, reset, and unsupported-WebGL fallback.
- Observation focus and accessible detail drawer.
- Search, inspection-only filtering, pagination, and CSV export.
- Shared inspection threshold and editable USD cost assumptions.
- Confusion counts, recall, precision, inspection workload, and hypothetical costs.
- Server-evaluated operating scenarios and one-feature median-replacement sensitivity.
- Calibrated random forest versus calibrated logistic baseline.
- Precision–recall and reliability charts, permutation importance, PSI, quality slices, and row-order stress evaluation.
- Downloadable PRD, TRD, UIRD, full-stack guide, model card, and evaluation JSON.
- Server health and validated prediction APIs.

## 5. Primary journeys

### 5.1 Inspect an observation

Open Risk workspace → choose quality scope → inspect the 3D landscape or queue → select an observation → read sensor values, recorded outcome, and feature sensitivity → send its values to Decision lab.

The table remains the keyboard-accessible route to every observation. Selecting a point does not issue a work order or modify an asset.

### 5.2 Compare policies

Choose threshold and inspection/failure costs → observe the counts and cost change → review false positives and missed failures → export the current policy.

The default threshold is frozen from calibration-set cost selection. User adjustments are exploratory test-set analyses and are not an unbiased new policy evaluation.

### 5.3 Evaluate a scenario

Set quality type and five sensor values → click Evaluate scenario → receive calibrated probability, decision status, and training-range warnings → change an input and evaluate again.

The result is cleared when inputs change, preventing stale results from being shown as current. Scenario predictions are associative model outputs, not interventions or guarantees of prevented failure.

### 5.4 Audit the science

Open Model evidence → compare baseline and forest → inspect calibration and subgroup variability → review the row-order stress test → download the evaluation report and model card.

## 6. Decision model

Let `I` be inspection count, `FN` missed observed failures, `C_i` inspection cost, and `C_f` missed-failure cost.

`policy_cost = I × C_i + FN × C_f`

`no_inspection_cost = observed_failures × C_f`

`hypothetical_reduction = no_inspection_cost − policy_cost`

The demonstration assumes every inspection on a failed observation prevents the full loss. It does not model inspection efficacy, downtime duration, staffing constraints, repair cost, or capacity. Negative reductions must remain visible. Dollar values are hypothetical assumptions.

Default assumptions: inspection $150; missed failure $12,000; calibration-selected threshold 0.005.

## 7. Acceptance criteria

| ID | Requirement | Acceptance |
|---|---|---|
| P01 | Working product first viewport | Initial screen exposes evaluated scope, results, risk workspace and filters |
| P02 | Scope accuracy | Quality filter updates plotted observations, queue and policy counts together |
| P03 | Policy accuracy | Confusion counts sum to scoped observations; exported policy matches visible inputs |
| P04 | Inference consistency | Portable server probability matches Python output; checked over all holdout rows |
| P05 | Input validity | Unknown fields, invalid types and out-of-bounds values produce a 400 response |
| P06 | Explainability honesty | Sensitivity is labeled nonadditive and noncausal; never presented as SHAP |
| P07 | Responsive use | Desktop two-column workspace; narrow screens stack without page overflow |
| P08 | Accessible alternative | Queue supports keyboard selection and remains usable without WebGL |
| P09 | Provenance | Synthetic nature, source, license, split and exclusions are visible |
| P10 | Reproducibility | Data hash, split IDs, environment pins, seed and model artifacts are committed |
| P11 | Documentation | PRD/TRD/UIRD, full-stack guide and model card available in project docs |
| P12 | Delivery | Deployed site and complete source package; GitHub publishing requires a writable target |

## 8. Success measures

For this benchmark, correctness and reviewability matter more than invented user adoption. Recorded evaluation metrics are AP, AUROC, Brier score, inspection count, recall, precision, missed failures, and bootstrapped AP uncertainty.

For a future field pilot, measure analyst task completion, alert burden per real machine-day, detection lead time, downtime, realized inspection costs, and incident outcomes. No such measurements exist in v1.

## 9. Exclusions

No live telemetry, predictive forecast horizon, remaining useful life, causal optimization, sensor ingestion, scheduling, maintenance work orders, customer data uploads, or persistent policy records. No fabricated real-time statuses or claimed realized savings. No in-product model retraining.

## 10. Risks and next validation gates

- Synthetic rule-generated labels inflate transfer expectations: prominently disclose the benchmark nature.
- Row dependence: random splitting may be optimistic; include a separate contiguous-row stress evaluation.
- Sparse failures: quality-H has few failures; display subgroup sample counts.
- Threshold overfitting: calibration and threshold selection use the same calibration split; a production pipeline should reserve a policy-validation split or nested validation.
- Calibration depends on prevalence: require deployment-population recalibration and prospective monitoring.
- Operational transfer: obtain dated observations, persistent equipment IDs and a clear forecast horizon before claiming preventive capability.

## 11. Release boundary

v1 is a reproducible demonstration suitable for a portfolio and certification discussion. Field operation requires a monitored pilot, stakeholder cost validation, prospective temporal evaluation, security/load assessment, incident response, and rollback procedures.
