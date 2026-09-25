#!/usr/bin/env python3
"""Kaggle-hosted autonomous worker for this repository.

The worker is intentionally limited to repository-level automation:
- creates/uses an isolated Git branch;
- installs development checks;
- optionally invokes Aider through an OpenAI-compatible API;
- validates pytest + ruff before committing;
- pushes only to the worker branch.

KLayout GUI/runtime acceptance is NOT performed in Kaggle.
"""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BASE_BRANCH = os.getenv("KAGGLE_BASE_BRANCH", "master")
WORK_BRANCH = os.getenv("KAGGLE_WORK_BRANCH", "kaggle/autonomous-worker")
DEFAULT_TASK_FILE = REPO_ROOT / "kaggle" / "AGENT_TASK.md"
MAX_AGENT_PASSES = int(os.getenv("KAGGLE_MAX_AGENT_PASSES", "2"))

FORBIDDEN_SUFFIXES = {".gds", ".oas", ".oasis"}
FORBIDDEN_NAME_PARTS = (
    ".env",
    "credential",
    "credentials",
    "secret",
    "secrets",
    "token",
    "password",
)


def run(
    args: list[str],
    *,
    cwd: Path = REPO_ROOT,
    env: dict[str, str] | None = None,
    check: bool = True,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(args))
    return subprocess.run(
        args,
        cwd=str(cwd),
        env=env,
        text=True,
        check=check,
        capture_output=capture,
    )


def read_setting(name: str, *, required: bool = False) -> str | None:
    value = os.getenv(name)
    if value:
        return value.strip()

    try:
        from kaggle_secrets import UserSecretsClient  # type: ignore

        value = UserSecretsClient().get_secret(name)
        if value:
            return value.strip()
    except Exception:
        value = None

    if required:
        raise RuntimeError(
            f"Missing {name}. Add it under Kaggle Notebook -> Add-ons -> Secrets "
            "and attach it to the notebook."
        )
    return None


def ensure_git_repo() -> None:
    if not (REPO_ROOT / ".git").exists():
        raise RuntimeError(
            "Run this script from a Git clone of "
            "aoa-create/klayout-microfluidic-trapping-array."
        )


def prepare_branch() -> None:
    run(["git", "fetch", "origin", BASE_BRANCH])
    remote = run(
        ["git", "ls-remote", "--heads", "origin", WORK_BRANCH],
        capture=True,
    )
    if remote.stdout.strip():
        run(["git", "fetch", "origin", WORK_BRANCH])
        run(["git", "checkout", "-B", WORK_BRANCH, f"origin/{WORK_BRANCH}"])
        rebase = run(
            ["git", "rebase", f"origin/{BASE_BRANCH}"],
            check=False,
            capture=True,
        )
        if rebase.returncode != 0:
            run(["git", "rebase", "--abort"], check=False)
            raise RuntimeError(
                "Worker branch could not be rebased cleanly onto the base branch. "
                "Resolve the branch conflict in GitHub before the next Kaggle run."
            )
    else:
        run(["git", "checkout", "-B", WORK_BRANCH, f"origin/{BASE_BRANCH}"])

    run(["git", "config", "user.name", "kaggle-autonomous-worker"])
    run(["git", "config", "user.email", "kaggle-worker@users.noreply.github.com"])


def install_repo_checks() -> None:
    run([sys.executable, "-m", "pip", "install", "-q", "-e", ".[dev]"])


def ensure_aider() -> str:
    aider = shutil.which("aider")
    if aider:
        return aider

    run([sys.executable, "-m", "pip", "install", "-q", "aider-install"])
    installer = shutil.which("aider-install")
    if not installer:
        raise RuntimeError("aider-install was installed but its executable was not found.")
    run([installer])

    aider = shutil.which("aider")
    if not aider:
        # aider-install commonly installs into ~/.local/bin.
        candidate = Path.home() / ".local" / "bin" / "aider"
        if candidate.exists():
            aider = str(candidate)
    if not aider:
        raise RuntimeError("Aider installation completed but the aider executable was not found.")
    return aider


def validation() -> tuple[bool, str]:
    commands = [
        [sys.executable, "-m", "pytest", "-q"],
        [sys.executable, "-m", "ruff", "check", "."],
    ]
    outputs: list[str] = []
    ok = True

    for command in commands:
        result = run(command, check=False, capture=True)
        outputs.append(f"$ {' '.join(command)}\n{result.stdout}\n{result.stderr}")
        if result.returncode != 0:
            ok = False

    report = "\n\n".join(outputs)
    print(report)
    return ok, report


def load_task() -> str | None:
    override = read_setting("KAGGLE_AGENT_TASK")
    if override:
        return override
    if DEFAULT_TASK_FILE.exists():
        text = DEFAULT_TASK_FILE.read_text(encoding="utf-8").strip()
        return text or None
    return None


def sanitized_aider_env(api_key: str, api_base: str) -> dict[str, str]:
    # Do not expose GitHub/Kaggle credential material to the coding agent.
    blocked = ("TOKEN", "SECRET", "PASSWORD", "API_KEY", "ACCESS_KEY", "PRIVATE_KEY")
    env = {
        key: value
        for key, value in os.environ.items()
        if not any(marker in key.upper() for marker in blocked)
    }
    env["OPENAI_API_KEY"] = api_key
    env["OPENAI_API_BASE"] = api_base
    env["AIDER_DISABLE_PLAYWRIGHT"] = "true"
    env["AIDER_SUGGEST_SHELL_COMMANDS"] = "false"
    env["AIDER_DETECT_URLS"] = "false"
    env["AIDER_AUTO_COMMITS"] = "false"
    return env


def run_agent(task: str, validation_report: str) -> None:
    api_key = read_setting("LLM_API_KEY", required=True)
    api_base = read_setting("LLM_BASE_URL", required=True)
    model = read_setting("LLM_MODEL", required=True)
    assert api_key and api_base and model

    aider = ensure_aider()
    model_arg = model if "/" in model and model.startswith("openai/") else f"openai/{model}"
    env = sanitized_aider_env(api_key, api_base)

    base_instruction = f"""
You are the Kaggle autonomous worker for this repository.

Mandatory constraints:
1. Read and obey AGENTS.md, README.md and SECURITY.md before editing.
2. Preserve the documented coordinate convention, parameter names, units,
   deterministic-seed behavior, trap geometry, margins, disorder equations,
   IO geometry and layer semantics unless the task explicitly requires a
   versioned migration.
3. Kaggle does not provide KLayout GUI acceptance here. Never claim that
   KLayout geometry execution, library registration or GUI behavior was
   validated unless there is actual KLayout execution evidence.
4. Do not add credentials, telemetry, network access to the macro, generated
   GDS/OASIS files, local KLayout settings or confidential mask data.
5. Keep changes minimal and testable. Update tests/docs for functional changes.
6. Do not commit; the outer worker validates and commits only after checks pass.

Task:
{task}

Current repository validation output:
{validation_report}
""".strip()

    result = run(
        [
            aider,
            "--model",
            model_arg,
            "--message",
            base_instruction,
            "--yes-always",
            "--no-auto-commits",
            "--no-suggest-shell-commands",
            "--disable-playwright",
            "--no-detect-urls",
        ],
        env=env,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Aider exited with status {result.returncode}.")


def changed_paths(staged: bool = False) -> list[str]:
    args = ["git", "diff", "--name-only"]
    if staged:
        args.insert(2, "--cached")
    result = run(args, capture=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def guard_staged_files(paths: list[str]) -> None:
    for raw in paths:
        path = Path(raw)
        lower = raw.lower()
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            raise RuntimeError(f"Refusing to commit generated layout file: {raw}")
        if any(part in lower for part in FORBIDDEN_NAME_PARTS):
            raise RuntimeError(f"Refusing to commit possible credential/sensitive file: {raw}")


def push_with_token() -> None:
    github_token = read_setting("GITHUB_TOKEN", required=True)
    assert github_token

    with tempfile.TemporaryDirectory(prefix="kaggle-git-") as tmp:
        askpass = Path(tmp) / "askpass.sh"
        askpass.write_text(
            "#!/bin/sh\n"
            "case \"$1\" in\n"
            "  *Username*) printf '%s\\n' 'x-access-token' ;;\n"
            "  *) printf '%s\\n' \"$GITHUB_TOKEN\" ;;\n"
            "esac\n",
            encoding="utf-8",
        )
        askpass.chmod(askpass.stat().st_mode | stat.S_IXUSR)

        env = os.environ.copy()
        env["GITHUB_TOKEN"] = github_token
        env["GIT_ASKPASS"] = str(askpass)
        env["GIT_TERMINAL_PROMPT"] = "0"
        env.pop("LLM_API_KEY", None)

        run(["git", "push", "-u", "origin", WORK_BRANCH], env=env)


def main() -> int:
    ensure_git_repo()
    prepare_branch()
    install_repo_checks()

    initial_ok, report = validation()
    task = load_task()

    model_configured = all(
        read_setting(name)
        for name in ("LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL")
    )

    if task and model_configured:
        for attempt in range(1, MAX_AGENT_PASSES + 1):
            print(f"\n=== Agent pass {attempt}/{MAX_AGENT_PASSES} ===")
            run_agent(task, report)
            passed, report = validation()
            if passed:
                break
            task = (
                "Repair only the validation failures shown below while obeying all "
                "repository constraints. Do not broaden scope.\n\n" + report
            )
        else:
            raise RuntimeError("Validation still fails after the configured agent passes.")
    elif not initial_ok:
        raise RuntimeError(
            "Repository checks failed and no complete LLM configuration was provided."
        )
    else:
        print(
            "LLM configuration not complete; verification-only mode finished successfully. "
            "Add LLM_API_KEY, LLM_BASE_URL and LLM_MODEL to enable the autonomous agent."
        )

    passed, _ = validation()
    if not passed:
        raise RuntimeError("Final validation failed; refusing to commit or push.")

    status = run(["git", "status", "--porcelain"], capture=True)
    if not status.stdout.strip():
        print("Working tree is clean. Nothing to commit or push.")
        return 0

    run(["git", "add", "-A"])
    staged = changed_paths(staged=True)
    guard_staged_files(staged)

    if not staged:
        print("No staged changes remain.")
        return 0

    run(["git", "commit", "-m", "chore(kaggle): autonomous worker update"])
    push_with_token()
    print(f"Worker changes pushed to origin/{WORK_BRANCH}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
