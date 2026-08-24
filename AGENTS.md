# BioMEMS Design-to-Fab Hub Development Protocol

## Scope and safety boundary

This repository is being evolved from a third-party KLayout PCell baseline into
the BioMEMS Design-to-Fab Hub. It is research software. It must not claim
clinical diagnostic performance, fabrication approval, institution-specific
process qualification, or hardware control.

## Release invariant

Each release must add exactly one bounded primary capability and one directly
related GUI milestone. A release is complete only when all of the following are
recorded:

1. automated checks pass;
2. the relevant GUI opens in a real application window;
3. the new GUI action is manually smoke-tested;
4. the current-state and changelog records are updated; and
5. the release commit and tag are created.

Do not bundle unrelated features into a release.

## Upstream and legacy identity

`trapping_array_pcell.lym` is the imported upstream baseline. Do not remove or
rewrite its copyright, attribution, publication reference, or licence evidence.
User-facing legacy names may only be replaced in the dedicated identity-cleanup
release. Preserve the mapping and rationale in `THIRD_PARTY_NOTICES.md`.

## Required reading before changes

1. `docs/PROJECT_EXECUTION_PROTOCOL.md`
2. `docs/CURRENT_STATE.md`
3. `docs/ROADMAP.md`
4. `THIRD_PARTY_NOTICES.md`
5. `docs/DELIVERY_PLAN.md`
