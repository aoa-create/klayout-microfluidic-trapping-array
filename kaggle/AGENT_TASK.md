# Default Kaggle autonomous task

Read `AGENTS.md`, `README.md`, `SECURITY.md`, `trapping_array_pcell.lym`
and the repository tests before making any change.

Run the repository-level validation and inspect the current code for one small,
clear, testable reliability or maintainability defect that can be corrected
without changing the documented scientific/fabrication semantics.

If such a defect exists:

1. implement the smallest correct fix;
2. add or update an automated test when the change is functional;
3. update documentation only when behavior or usage changes;
4. keep the documented geometry, coordinate convention, dimensions, disorder
   equations, deterministic seed behavior, IO geometry and layer semantics
   unchanged;
5. do not claim KLayout GUI/runtime acceptance from Kaggle.

If the repository is already clean and there is no well-supported change to
make, leave the working tree unchanged. Do not invent work merely to create a
commit.
