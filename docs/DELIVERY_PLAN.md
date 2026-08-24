# Fast Delivery Plan

## Operating model

The project advances as a sequence of small, independently verifiable releases.
The daily automation takes only the first unfinished item below. It may not
start a later release while the current release is missing its required evidence.

## Priority queue

### P0 — complete V0.0.1 baseline

1. Install or locate KLayout.
2. Import `trapping_array_pcell.lym` without modifying it.
3. Confirm that the Trapping Array library appears in KLayout.
4. Place one PCell and record the GUI smoke-test evidence.
5. Update `docs/CURRENT_STATE.md`, then create the V0.0.1 tag.

### P1 — V0.1.0 identity cleanup

One capability: replace legacy user-facing identity with BioMEMS Design-to-Fab
Hub identity while preserving third-party provenance outside the user workflow.

GUI acceptance: a modern Hub-branded desktop window opens and identifies the
upstream geometry component as an imported, attributed dependency.

### P2 — V0.2.0 project home

One capability: create or open a local Hub project.

GUI acceptance: the modern project-home window creates a new empty project and
reopens it without data loss.

### P3 — V0.3.0 device manifest

One capability: create and validate one device manifest.

GUI acceptance: the Manifest form highlights missing required fields and saves
a valid JSON file only when the form is complete.

### P4 — V0.4.0 parametric design

One capability: configure one trapping-array design from the manifest.

GUI acceptance: the Design workspace changes the displayed parameter summary
and prevents invalid values from being exported.

## Fast-track rules

- Prefer a thin vertical slice over new abstractions.
- Reuse the imported PCell rather than copying or silently rewriting it.
- Keep every sample synthetic and visibly labelled as such.
- Treat KLayout availability, a required licence clarification, or a request to
  push externally as an explicit checkpoint; do not guess past it.
- After every completed release, stop and record evidence before beginning the
  next release.

