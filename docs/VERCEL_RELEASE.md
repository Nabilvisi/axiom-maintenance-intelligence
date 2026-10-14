# Vercel release verification

Verified 13 October 2026 (Asia/Jakarta).

- Public application: https://axiom-maintenance-intelligence.vercel.app/
- GitHub repository: https://github.com/Nabilvisi/axiom-maintenance-intelligence
- Application migration commit: `0760c6f8d12679838165e58f1fc7bb0901c5bea7`.
- Initial Vercel production deployment: `dpl_9RcSnMAko68xgamRTjypHRKsQA3v`, READY, source Git, build duration about 85 seconds.
- Framework: Next.js 16.3.4, React 19.2.6, Node 24, pnpm 11.25.0. Build uses the supported webpack compiler because local Turbopack failed launching its CSS child worker.
- Vercel Git integration builds the repository's `main` branch automatically. The separate connector create-deployment operation returned a scope authorization error; the Git-triggered production deployment succeeded.

## Fresh checks

- Strict TypeScript check and complete Next.js production build passed.
- All 30 Python/JavaScript fixtures passed with maximum probability error zero.
- All 2,000 holdout predictions and all 10,000 split rows verified. Default policy: TP 66, FP 148, FN 2, TN 1,784.
- Real route-handler checks passed: valid response 200, four invalid requests 400, declared and streamed oversized bodies 413, no-store prediction cache policy.
- Local and public HTTP smoke checks passed: page, health, prediction and benchmark 200; three invalid prediction requests 400; oversized request 413; benchmark contains 2,000 observations.
- Playwright exercised the public decision scenario, observation search and selection, detail drawer and Escape dismissal, empty search and recovery, keyboard threshold changes and reset, model evidence and project-docs tabs.
- Real filtered CSV export contains its header plus the selected `OBS-00328` row, with source sensor values and threshold 0.005.
- Documentation downloads returned 200.
- Desktop screenshot (1440px) and mobile screenshot (390px) were visually inspected. Mobile layout did not overflow the viewport; drawer worked under reduced-motion emulation. The 3D point cloud rendered.
- Browser console check: zero errors and zero warnings in the checked session.

## Known limits

The inherited UI has seven lint findings: five `react-hooks/set-state-in-effect` findings (`app/page.tsx` lines 25, 27, 29, 32 and `components/risk-landscape.tsx` line 8), one `react-hooks/refs` finding (`app/page.tsx` line 33), and one `@next/next/no-html-link-for-pages` finding (`app/page.tsx` line 40). The migration does not claim a clean lint run. These files were preserved from the original export.

Checks are bounded product/deployment verification, not screen-reader certification, load testing, external security review, prospective scientific validation, or field qualification. Web Analytics and Speed Insights are not enabled. No realized maintenance benefit is claimed.

Local evidence is under ignored `outputs/`: desktop/mobile screenshots, downloaded CSV, browser acceptance script and lint JSON. The original Sites validation record remains historical; this document records the migration checks.
