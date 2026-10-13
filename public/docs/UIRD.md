# Axiom — User Interface Requirements Document

Version 1.0 · 8 October 2026

## 1. Experience thesis

A calm industrial analysis workspace: dark graphite, precise typography, lime decision highlights, cyan data, and coral elevated risk. The first viewport shows actual model-backed work rather than a marketing landing page.

3D is an exploratory visualization of operating states, not decorative equipment art. Tables and numeric outcomes remain the primary accessible evidence.

## 2. Information architecture

| View | User task | Content |
|---|---|---|
| Risk workspace | Find what needs attention | Quality scope, four KPIs, 3D plot, observation focus, queue, policy |
| Decision lab | Compare assumptions and scenarios | Shared policy controls, confusion matrix, costs, five-sensor scenario |
| Model evidence | Challenge the prediction system | Baseline, AP/AUROC/Brier, curves, importance, PSI, quality slices, ordered test |
| Project docs | Understand and reproduce | PRD/TRD/UIRD downloads, architecture, source provenance, model card |
| Observation sheet | Inspect one operating state | Sensors, recorded outcome, probability, feature sensitivity, scenario transfer |

Main navigation is an accessible tab list. Each main view has one purpose; dialogs do not introduce independent pages or hidden persistence.

## 3. Visual tokens

| Token | Value | Purpose |
|---|---|---|
| Background | #0b121b | Main canvas |
| Surface | #101b27 | Cards and sections |
| Border | #263542 | Quiet separation |
| Primary text | #edf3f8 | Headings and numbers |
| Secondary text | #9cabbc | Context and labels |
| Lime | #b4ee6e | Inspection policy and positive decision emphasis |
| Cyan | #6bd5ef | Secondary quantitative evidence |
| Coral | #fc987b | Elevated risk and missed-failure attention |
| Muted point | #397a92 | Below-threshold observations |

System sans-serif typography uses Inter if present, followed by Segoe UI and Arial; no remote font is required. Monospace is used for observation IDs, model versions and compact numeric details. Body text is 16px. Core control text is 13–14px where space is constrained; contextual metadata can be 10–12px. Tiny chart labels are secondary to table and detail equivalents. Future accessibility review should reconsider metadata sizes at high zoom.

Headings have restrained tracking; KPI values use tabular numbers. Cards use a 7–10px radius. Buttons have text/icon labels, clear focus outlines and disabled states.

## 4. Desktop layout

- Header: brand at left, synthetic benchmark and model identity at right.
- Main content maximum width 1,500px with 44px side padding.
- Page introduction is brief; tabs and the working surface remain prominent.
- Four metric cards in one row.
- Risk landscape is the wide panel; selected observation is the narrow 310–340px panel.
- Queue and shared policy panel repeat the same visual alignment below.
- Evidence uses a two-column chart/panel layout.
- Project document cards use three equal columns.

## 5. Responsive layout

| Width | Behavior |
|---|---|
| >1,100px | Four KPI columns; main visualization plus observation rail |
| 821–1,100px | Reduced padding and rail width; controls remain full size |
| ≤820px | Two KPI columns; stacked main panels; evidence and decision views single column |
| ≤560px | 16px side padding; scrollable tab row; compact header; stacked queue controls; sheet fits viewport |

Table overflow is contained to its table wrapper; the page must not scroll horizontally. Navigation may scroll horizontally to retain readable tab labels. 3D consumes touch gestures only within its plot surface. The rest of the page remains normally scrollable. Metric text must wrap rather than overlap. At 200% text enlargement the stacked layouts should remain operable; this needs a browser acceptance review.

## 6. Risk landscape

Coordinates use original measurements normalized into a single 3D operating space:

- X: tool wear, minutes.
- Y: torque, Nm.
- Z: rotational speed, rpm.

A grid and unit labels establish orientation. Default camera provides depth without hiding all low-risk points. Users drag to orbit, scroll/pinch to zoom, select a point, and reset the camera. A wireframe marker highlights the selected observation.

Point colors communicate calibrated probability categories: below inspection threshold, inspection candidate, and ≥25% high risk. High risk is an independent fixed category; when the inspection threshold exceeds 25%, some high-risk points are below the current inspection policy. The queue always shows the actual threshold-based decision.

The chart represents all observations in the current quality scope. The point tooltip includes ID and risk. Table selection provides the complete keyboard route to the same details. WebGL failure produces a 2D wear-versus-torque fallback and points users to the queue.

## 7. Queue and observation details

- Default sort: descending risk, then observation ID.
- Search: case-insensitive observation ID.
- Filter: all observations or inspection candidates only.
- Pagination: seven rows; changing scope/search/threshold resets the page.
- Selection: click an ID to open details; selected row is visually marked.
- Export: current filtered queue to CSV, with threshold and decision included.
- Empty state: no-match text and a clear-filter action.

Detail sheet includes operating readings with units, recorded target outcome and calibrated risk. Feature sensitivity is clearly described as median replacement, nonadditive and noncausal. An action copies original readings to Decision lab and closes the sheet.

## 8. Policy interactions

Inspection threshold uses an accessible slider from 0.5% to 95%, step 0.5%. Costs are numeric inputs with bounded positive values. Changes immediately update scoped inspection counts, recall/precision, confusion matrix and cost calculations.

Risk workspace and Decision lab share one policy state. Reset restores the frozen calibration-selected policy and cost assumptions. Dollar values use hypothetical USD formatting; no implied geographic currency conversion.

No notifications suggest that changing policy has scheduled actual inspections. CSV/JSON downloads are local exports of analysis results.

## 9. Operating scenario

Quality uses an accessible select. Five sensor sliders display value and unit beside their label. Clicking Evaluate scenario sends the current values to the server. The button shows progress and disables during the request. Failure produces visible error text. Result includes risk, threshold decision and any range warnings.

Changing any sensor clears the old result. No stale score remains beside updated values. Selecting a recorded observation and choosing Use in operating scenario initializes all six values together.

## 10. Model evidence

- Metric cards: AP, AUROC, Brier, failure prevalence.
- Baseline comparison table: same calibration/test procedure.
- Precision–recall plot: axes from 0–1, explicit labels and metric caption.
- Reliability plot: occupied bins with sample count annotations.
- Importance list: feature name, AP decrease, five-repeat standard deviation.
- Data quality: missing/duplicate IDs, feature PSI and split counts.
- Stress test: separate row-order model results and its limitations.
- Slice table: L/M/H row counts, failures, AP and default recall.
- Limitations panel: synthetic nature, missing forecast horizon, temporal caveat and field validation needs.

Color is never the only explanation of an outcome: numeric scores, status words and recorded outcomes accompany it. No implied statistical confidence badge is inferred from a green status light.

## 11. Loading, error and success states

| Situation | Required feedback |
|---|---|
| Initial data loading | Named benchmark loading message |
| Benchmark fetch failure | Clear error and Try again |
| 3D module loading | Preparing visualization text |
| Unsupported WebGL | Fallback chart plus queue alternative |
| Explanation pending | Calculating feature sensitivity |
| Explanation request failure | Specific text and reselection guidance |
| Scenario pending | Evaluating label, disabled button |
| Scenario input/server failure | Visible alert text |
| CSV exported | Brief check-mark Exported feedback |
| Unexpected route error | Retry screen |

## 12. Accessibility and motion

Use semantic headings, labeled fields, native buttons and installed accessible primitives. All control and download actions have discernible names. Focus styles remain visible. The sheet must trap/restore focus through the primitive. Tabs are keyboard navigable; sliders and selects use their accessible primitives.

The 3D canvas has descriptive text, but is not the sole means to inspect observations. Respect prefers-reduced-motion; no auto-rotating camera or essential animation is used. Three.js renders on interaction/resize instead of an idle animation loop.

No claim of WCAG certification is made. Keyboard, screen-reader, contrast, zoom and device testing remain browser acceptance work.

## 13. UX acceptance review

Check desktop, 820px and 390px widths; 200% zoom; keyboard tab traversal; sheet close/restore focus; threshold extreme values; all quality filters; no-match query; last-page pagination; scenario error recovery; CSV/JSON downloads; WebGL disabled; and reduced motion.

The environment did not provide the required browser-control skill, so visual/browser QA is not claimed. TypeScript, numerical tests, HTTP API tests and deployment builds supply the automated verification available here.
