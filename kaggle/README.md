# Kaggle independent worker

This directory lets the repository run from a Kaggle Notebook without relying
on the Windows or Linux computers that normally host the project.

The Kaggle worker performs repository-level automation only. It does **not**
replace KLayout GUI/runtime acceptance testing.

## 1. Kaggle notebook settings

Create a new Kaggle Notebook and set:

- **Internet:** On
- **Accelerator:** None (CPU is sufficient for this repository)

Attach these Kaggle Secrets:

| Secret | Required | Purpose |
|---|---|---|
| `GITHUB_TOKEN` | only when changes must be pushed | Git push to the worker branch |
| `LLM_API_KEY` | for agent mode | OpenAI-compatible model API key |
| `LLM_BASE_URL` | for agent mode | API base URL, e.g. `https://integrate.api.nvidia.com/v1` |
| `LLM_MODEL` | for agent mode | Provider model id, e.g. `moonshotai/... ` |
| `KAGGLE_AGENT_TASK` | optional | Overrides `kaggle/AGENT_TASK.md` |

Kaggle Secrets are read with `kaggle_secrets.UserSecretsClient`; credentials
are not stored in this repository.

## 2. Start the worker

For the current test branch, run this single Kaggle cell:

```python
import os
import shutil
import subprocess
from pathlib import Path

repo_url = "https://github.com/aoa-create/klayout-microfluidic-trapping-array.git"
branch = "feat/kaggle-independent-worker"
workdir = Path("/kaggle/working/klayout-microfluidic-trapping-array")

if workdir.exists():
    shutil.rmtree(workdir)

subprocess.run(
    ["git", "clone", "--branch", branch, "--single-branch", repo_url, str(workdir)],
    check=True,
)
subprocess.run(
    ["python", "kaggle/run_worker.py"],
    cwd=workdir,
    check=True,
)
```

After this feature branch is merged, use `master` instead of
`feat/kaggle-independent-worker`.

## 3. Operating modes

### Verification-only mode

If the three LLM secrets are absent, the worker:

1. checks out/refreshes `kaggle/autonomous-worker`;
2. installs `.[dev]`;
3. runs `python -m pytest -q`;
4. runs `python -m ruff check .`;
5. exits without changing the repository when checks pass.

No GitHub token is required if nothing needs to be pushed.

### Autonomous agent mode

When `LLM_API_KEY`, `LLM_BASE_URL` and `LLM_MODEL` are all present, the
worker additionally:

1. installs Aider if necessary;
2. reads the task from `KAGGLE_AGENT_TASK` or `kaggle/AGENT_TASK.md`;
3. invokes the model through the configured OpenAI-compatible endpoint;
4. validates the resulting edits with pytest and Ruff;
5. makes one repair pass when validation fails, up to
   `KAGGLE_MAX_AGENT_PASSES` (default: 2);
6. commits only if validation passes;
7. pushes only to `kaggle/autonomous-worker`.

Aider's documented OpenAI-compatible mode uses `OPENAI_API_BASE`,
`OPENAI_API_KEY` and a model name prefixed with `openai/`. The worker sets
those values internally from Kaggle Secrets.

## 4. Isolation and safety

The worker deliberately does not push directly to `master`.

Before a commit it rejects:

- `.env` or credential/token/password-like files;
- generated `.gds`, `.oas` and `.oasis` files.

The Aider subprocess receives the model API credential but does not inherit the
GitHub token or Kaggle secret-service token. GitHub authentication is exposed
only to the final `git push` operation through a temporary `GIT_ASKPASS`
helper.

## 5. Scientific validation boundary

Kaggle can validate repository structure, Python tests, linting and text/code
changes. It must not be treated as evidence that:

- KLayout loaded the macro successfully;
- the PCell library registered in the GUI;
- generated geometry is fabrication-qualified;
- a foundry/process rule deck has passed.

Those claims still require the acceptance process defined in `AGENTS.md`.
