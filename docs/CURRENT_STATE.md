# Current State

## V0.0.1 baseline

- Status: V0.0.1 baseline complete; GUI smoke evidence recorded on 2026-08-28.
- Upstream source: `FattaccioliLab/klayout-microfluidic-trapping-array`.
- Pinned upstream commit: `307f65aa5be35dc0eda3ae8fb2f2a3e2435941dc`.
- Imported artifact: `trapping_array_pcell.lym`.
- Existing GUI host: KLayout macro/PCell interface.
- Local KLayout host: KLayout 0.30.11 at `%APPDATA%\KLayout\klayout_app.exe`.
- Macro import: `trapping_array_pcell.lym` imported and executed successfully;
  the Python macro is visible in Macro Development and registers the library.
- GUI smoke: the Libraries panel shows `Trapping Array - Microfluidic trapping
  arrays (Ruyssen et al. 2025)` and `TrapArray_A — Fixed grid`; an instance is
  present in `TRAPPING_ARRAY_P_CELL_SMOKE`.
- Evidence: `docs/evidence/v0.0.1-klayout-library-pcell.png` (GUI screenshot),
  `docs/evidence/v0.0.1-pcell-placement-smoke.gds` (26,244 bytes), and
  `docs/evidence/v0.0.1-pcell-smoke.log` (library/PCell/GDS smoke log).

## Observed upstream capability

The baseline provides two parameterized single-layer PDMS hydrodynamic trapping
arrays. It performs geometry feasibility checks in the KLayout workflow and can
generate GDS output. It does not provide a Hub project format, a modern Hub GUI,
process-traveler records, fabrication qualification, or experimental QC.

## V0.0.1 completion criteria

1. upstream origin and commit are recorded;
2. upstream notice and licence evidence are retained;
3. baseline verification script passes; and
4. after KLayout installation, the upstream macro is imported and its Libraries
   panel entry plus a PCell placement are manually smoke-tested before release.

## Scope boundary

This release is a GUI-verified baseline only. It does not claim fabrication,
clinical, institutional, or experimental qualification.
