> Hosting update (14 October 2026): this checkout runs Next.js on Vercel. See [Vercel migration](VERCEL_MIGRATION.md) and [release verification](VERCEL_RELEASE.md). The original Sites/Cloudflare instructions below are historical.

# Axiom — Full Stack Project Guide

A complete benchmark-to-decision data science product, authored for Nabil Visi Samawi.

## Product

Axiom helps an analyst inspect operating-state failure risk, compare hypothetical inspection policies, and audit the model evidence. It uses UCI AI4I 2020, a synthetic 10,000-row industrial benchmark. This is a portfolio demonstration with no real customer telemetry.

## Repository map

```text
app/                       React workspace, styles, layout and API routes
components/risk-landscape.tsx  Dynamically loaded Three.js exploration
components/ui/             Installed accessible UI primitives
lib/                       Feature engineering, server inference, schemas and types
ml/train.py                Reproducible Python training/evaluation/export
ml/requirements.txt        Pinned training dependencies
data/raw/ai4i2020.csv       Unmodified attributed UCI dataset
data/splits.json           Fixed disjoint train/calibration/test row indexes
artifacts/model.json       Portable forest and isotonic calibration
artifacts/metrics.json     Evaluation, uncertainty, slices and stress test
artifacts/parity-fixtures.json  Python probabilities for cross-runtime checks
public/benchmark.json      Frozen holdout observations and metrics
public/docs/               Website-downloadable copies of canonical documentation
docs/                      PRD, TRD, UIRD, model card and project guide
scripts/verify-science.mjs  Numerical and data contract verification
build/ and scripts/        Framework and Sites build integration
```

## Run the science

Use Python 3.12 and Node 22.13 or later.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ml/requirements.txt
python3 ml/train.py
```

The raw data is already included under its CC BY 4.0 license. Training writes model JSON, metrics, split indexes, parity fixtures and the website benchmark. Small floating-point differences across platforms can occur; compare probability tolerance rather than requiring every exported byte to match.

## Run the website

The project uses pnpm and its lockfile. With pnpm available:

```bash
pnpm install --frozen-lockfile
pnpm run dev
```

The Sites starter supports an execution profile that is local and ignored by Git. For a fresh portable checkout outside the managed environment, the framework launcher defaults to portable; preserve the scripts and lockfile. The standard dev command uses Vinext; deployment produces a Cloudflare-compatible Worker.

```bash
pnpm run typecheck
pnpm run test:science
pnpm run build
```

The training pipeline is offline Python; inference at runtime is TypeScript. No Python process or external ML endpoint is needed by the deployed site.

## API example

```bash
curl -X POST http://localhost:5173/api/predict \
  -H 'Content-Type: application/json' \
  -d '{"type":"L","air":300,"process":310,"speed":1500,"torque":40,"wear":100}'
```

The response includes calibrated risk, one-feature sensitivity, version and range warnings. See TRD.md for the contract and input bounds. The local port above is the portable development convention; managed Sites preview uses its supervised endpoint.

## Review documents

1. PRD.md: what the product solves and how success is assessed.
2. TRD.md: architecture, data/model contracts, evaluation and deployment.
3. UIRD.md: interface design and interaction rules.
4. MODEL_CARD.md: intended use, measured results and evidence limits.
5. VALIDATION.md: checks completed and checks unavailable.

## GitHub publication

Use a dedicated repository named `axiom-maintenance-intelligence`. Include the complete project, data attribution, lockfile and model artifacts. Never upload node_modules, build output, runtime state, credentials or temporary environments.

The connected GitHub app can write existing repositories but cannot create a new one. The project is prepared for a dedicated target; repository creation through the browser needs user permission, or the user can provide an existing empty writable repository.

## Portfolio narrative

Begin with the business decision, not the algorithm. Show how threshold changes inspection burden and misses. Explain calibration, leakage exclusions and the simpler baseline. Show the ordered-split drop, sparse quality-H subgroup and synthetic limitations. End with the concrete pilot plan needed to validate real value.

The project demonstrates practices associated with experienced data science work; it does not establish that its owner has ten years of professional experience.

