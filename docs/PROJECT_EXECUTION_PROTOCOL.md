# Project Execution Protocol

## Product direction

BioMEMS Design-to-Fab Hub will be a modern Windows-first research desktop
application for an auditable, design-to-experiment workflow around microfluidic
BioMEMS prototypes. It will begin with single-layer PDMS trapping-array layouts.

The final product uses a coherent PySide6/Qt6 interface. During the transition,
KLayout remains the verified geometry host for the upstream PCell. The final
product must make the boundary between imported geometry, advisory checks and
human engineering review visible.

## Working rule

One version equals one bounded capability. Every version must include one GUI
surface for that capability; no hidden-only features are accepted. A capability
is not complete if a new window cannot be opened and exercised manually.

## Evidence required per release

- source revision and dependency versions;
- automated-check output;
- GUI smoke-test result and screenshot path;
- known limitations;
- changelog entry; and
- commit and annotated tag.

## Identity cleanup rule

Legacy branding is removed in one dedicated, reviewable release. It applies only
to user-facing text, window titles, icons, default project names and packaging
metadata. Third-party attributions, licences, commit IDs and scientific
references stay intact in notices and provenance records.

## Non-negotiable boundaries

- Advisory geometry checks are not fabrication approval.
- Synthetic examples are not experimental or clinical performance evidence.
- The application does not command laboratory equipment.
- No patient-identifiable data belongs in the project format.
