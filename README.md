# Axiom — Maintenance Intelligence

A complete data science decision product: calibrated equipment failure classification, a responsive interactive 3D workspace, inspection-policy economics, and reproducible model evidence.

Built for Nabil Visi Samawi. This project demonstrates experienced data science practice; it does not claim ten years of personal experience or real production impact.

## Explore

- **Risk workspace:** all 2,000 held-out observations, quality filters, 3D selection, searchable queue, detail drawer and CSV export.
- **Decision lab:** shared policy threshold/costs, confusion counts, hypothetical costs and server-scored sensor scenarios.
- **Model evidence:** calibrated baseline comparison, PR/reliability curves, importance, PSI, quality slices, bootstrap uncertainty and row-order stress evaluation.
- **Project docs:** PRD, TRD, UIRD, full-stack guide and model card.

## Measured benchmark results

| Evaluation | AP | AUROC | Brier |
|---|---:|---:|---:|
| Logistic baseline, calibrated | 0.359 | 0.924 | 0.0257 |
| Random forest, calibrated | 0.849 | 0.985 | 0.0086 |
| Separate row-order stress refit | 0.701 | 0.920 | 0.0076 |

Default policy: 214 inspections, 66 captured failures and 2 missed failures out of 68 positive test labels. The default 0.5% threshold is selected on calibration data with hypothetical costs, not test optimization.

**Data honesty:** UCI AI4I 2020 is a synthetic 10,000-row benchmark. Failure classification concerns a recorded operating state, not a forecast horizon. Observations are not proven unique physical machines. No live telemetry, realized savings or causal maintenance effects are claimed.

## Full stack

React + TypeScript + accessible Shadcn/Radix controls + Three.js; Next.js server APIs; portable calibrated-forest inference; Python/scikit-learn training; committed artifacts and a source-data hash. The website does not need a Python runtime or API key. Sessions do not persist policies to a database.

## Run

Use Node 24 and pnpm 11.25.0 (Node 22.13+ is supported by the application).

```bash
pnpm install --frozen-lockfile
pnpm run dev
pnpm run typecheck
pnpm run test:science
pnpm run test:api
pnpm run build
```

To reproduce the model:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ml/requirements.txt
python3 ml/train.py
```

Use Python 3.12.14 or compatible Python 3.12. Generated probabilities can vary at floating-point precision across environments; the parity checks use numerical tolerances.

## Documentation

- [PRD](docs/PRD.md): business decision, scope, users and acceptance criteria.
- [TRD](docs/TRD.md): architecture, contracts, evaluation, security and deployment.
- [UIRD](docs/UIRD.md): interface, interactions, responsiveness and accessibility.
- [Full stack guide](docs/FULL_STACK_PROJECT.md): repository map and execution.
- [Model card](docs/MODEL_CARD.md): intended use and measured limitations.
- [Validation](docs/VALIDATION.md): checks completed and limitations.

## Data and software licenses

Software: MIT. Dataset: AI4I 2020, UCI, CC BY 4.0, DOI https://doi.org/10.24432/C5HS5C. See [attribution](data/ATTRIBUTION.md). Original CSV is unmodified; model probabilities, derived features and benchmark snapshots are project adaptations.

## GitHub and hosting

This checkout uses Next.js on Vercel. Source: https://github.com/Nabilvisi/axiom-maintenance-intelligence. See [Vercel migration](docs/VERCEL_MIGRATION.md) for hosting settings and current verification scope. The original ChatGPT Sites export is preserved separately.

## Production boundary

This is a functional portfolio benchmark, not production-certified equipment software. Real operation requires temporal/grouped validation, forecast definition, operational cost/efficacy measurement, prospective monitoring and security/load review. Browser UI QA has not been completed in the current environment.

