from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path


def run(command: list[str], *, cwd: Path) -> str:
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    environment["PYTHONUTF8"] = "1"
    completed = subprocess.run(  # noqa: S603 - every executable is an absolute path created by this script
        command,
        cwd=cwd,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = completed.stdout + completed.stderr
    if completed.returncode:
        raise RuntimeError(f"Command failed ({completed.returncode}): {' '.join(command)}\n{output}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Install a wheel in a clean environment and smoke-test its CLI.")
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()
    wheel = args.wheel.resolve(strict=True)

    with tempfile.TemporaryDirectory(prefix="mcpsec-wheel-smoke-") as temporary:
        root = Path(temporary)
        environment = root / "venv"
        venv.EnvBuilder(with_pip=True).create(environment)
        scripts = environment / ("Scripts" if sys.platform == "win32" else "bin")
        python = scripts / ("python.exe" if sys.platform == "win32" else "python")
        command = scripts / ("mcpsec.exe" if sys.platform == "win32" else "mcpsec")

        run([str(python), "-m", "pip", "install", "--disable-pip-version-check", str(wheel)], cwd=root)
        run([str(python), "-m", "pip", "check"], cwd=root)
        version = run([str(command), "--version"], cwd=root)
        help_text = run([str(command), "--help"], cwd=root)
        demo = run([str(command), "demo"], cwd=root)
        if not version.startswith("mcpsec ") or "Defensive static analysis" not in help_text:
            raise RuntimeError("Installed CLI version/help smoke test returned unexpected output")
        if "metadata_test_only" not in demo:
            raise RuntimeError("Installed demo did not scan the bundled catalog")
        print("Clean-wheel smoke test passed: --version, --help, and demo")


if __name__ == "__main__":
    main()
