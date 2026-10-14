> Hosting update (14 October 2026): this checkout runs Next.js on Vercel. See [Vercel migration](VERCEL_MIGRATION.md) and [release verification](VERCEL_RELEASE.md). The original Sites/Cloudflare instructions below are historical.

# Validation record

Release v1 · 8 October 2026

## Completed

- Python training pipeline ran successfully on the bundled 10,000-row source.
- Train/calibration/test splits are disjoint and cover every source row.
- Thirty full-precision Python/JavaScript fixtures: maximum probability error 0 in the checked environment.
- All 2,000 displayed holdout predictions agree with Python to the six-decimal display tolerance.
- All held-out observations satisfy the input schema.
- Six invalid schema cases rejected; training-range warnings and finite sensitivity verified.
- Default policy TP=66, FP=148, TN=1784, FN=2 agrees with frozen evaluation.
- Real prediction route tested in-process with Web Request/Response objects: valid 200, four invalid cases 400, declared and streamed oversized bodies 413, no-store cache policy.
- TypeScript strict typecheck passed.
- Production framework build passed.
- GitHub Actions workflow is configured to run typecheck, numerical tests, API route tests and production build. A remote run is not claimed before GitHub publication.

## Unavailable / not claimed

- Browser screenshots, mobile-device interaction testing, screen-reader testing and 200% zoom acceptance: required browser-control skill unavailable.
- Supervised preview reports running, but HTTP gateway requests return 502 from this environment. Direct endpoint smoke testing did not pass; the real route handler passed in-process instead. Production availability is checked through the hosting deployment-status operation.
- Native WebMCP registration/execution: no permitted supported browser context.
- Operational/pilot impact, realized cost savings, future lead-time performance and field robustness.
- Public load/security certification or external penetration testing.

## Reproduce

```bash
pnpm run typecheck
pnpm run test:science
pnpm run test:api
pnpm run build
```

The separate scripts/smoke-api.mjs supports an explicit AXIOM_TEST_BASE pointing to a reachable local deployment. It checks page, benchmark, health and prediction HTTP responses; do not count it as passed in this release record.

