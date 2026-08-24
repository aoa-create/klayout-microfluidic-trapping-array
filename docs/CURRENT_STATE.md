# Current State

## V0.0.1 baseline

- Status: baseline documentation and integrity controls in progress.
- Upstream source: `FattaccioliLab/klayout-microfluidic-trapping-array`.
- Pinned upstream commit: `307f65aa5be35dc0eda3ae8fb2f2a3e2435941dc`.
- Imported artifact: `trapping_array_pcell.lym`.
- Existing GUI host: KLayout macro/PCell interface.
- Local KLayout command availability: not detected during baseline setup.

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
   panel entry is manually smoke-tested before the release is tagged.
