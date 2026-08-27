# Agent operating contract

## Repository purpose

This repository contains a KLayout Python macro (`trapping_array_pcell.lym`) that installs and registers the **Trapping Array** PCell library for hydrodynamic microfluidic trapping-array layouts.

## Required reading before changes

1. `README.md`
2. `SECURITY.md`
3. `trapping_array_pcell.lym`
4. `tests/`

## Non-negotiable rules

- Preserve the documented coordinate convention, parameter names, units and deterministic-seed behavior unless a versioned migration is explicitly documented.
- Do not claim that CI validates KLayout geometry execution when KLayout is not installed. The default CI performs repository and macro-structure checks only.
- Real PCell generation, library registration and GUI behavior require acceptance testing in a compatible KLayout installation before a release claim.
- Do not add network access, telemetry, credential access, shell execution or unrelated filesystem writes to the macro.
- The macro may write only its documented installed library files under the user's KLayout macro directory and user-selected layout outputs.
- Do not commit generated or proprietary GDS/OASIS layouts, local KLayout settings, credentials, tokens or confidential mask data.
- Treat DRC/fabrication suitability as an external engineering responsibility. This repository does not provide foundry approval or a qualified process rule deck.
- Keep scientific/fabrication assumptions explicit. Do not silently change trap geometry, margins, disorder equations, IO geometry or layer semantics.
- Any functional change must add or update automated tests and documentation.

## Definition of done

A change is complete only when:

- the intended source or documentation change is present;
- `python -m pytest -q` passes for repository-level checks;
- KLayout-dependent behavior is either tested in KLayout or explicitly recorded as not tested;
- documentation matches implemented behavior;
- no secrets, generated masks or confidential fabrication data are committed.
