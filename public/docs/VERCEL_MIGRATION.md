# Vercel migration

The original ChatGPT Sites export is preserved in the workspace ZIP. This checkout runs the existing React interface and prediction routes with Next.js 16 on Node 24. The trained model, dataset, benchmark snapshot, policy logic, and interface are preserved.

## Run

```sh
pnpm install --frozen-lockfile
pnpm run dev
pnpm run typecheck
pnpm run test:science
pnpm run test:api
pnpm run build
pnpm run start
```

Next.js uses port 3000 by default. Set `AXIOM_TEST_BASE` to the actual local or public URL when running `node scripts/smoke-api.mjs`.

## Hosting

GitHub source: https://github.com/Nabilvisi/axiom-maintenance-intelligence

Vercel project: axiom-maintenance-intelligence. Framework: Next.js. Node: 24.x. Build: `pnpm run build`. Install: `pnpm install --frozen-lockfile`. No API keys or database are required for the application.

The exported Cloudflare/Vinext build files and unused database starter are retained for provenance but excluded from the Next.js TypeScript project. They are not used by the application routes. ChatGPT authentication helpers and connector scaffolding are unused; this deployment does not provide ChatGPT authentication or connected-service access.

The original validation document describes checks from the Sites release. Current migration checks and deployment evidence are recorded separately; historical claims are not fresh verification.

## Scope

This remains a portfolio decision-support demonstration using synthetic UCI AI4I 2020 data. Migration does not establish operational qualification, prospective failure prediction, causal maintenance benefits, or realized savings.
