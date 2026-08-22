"""Shared scaffolding for check-traceability.sh's own test suite.

Every test builds a minimal, disposable project under tmp_path and runs the
real script via subprocess against it -- the same shape of scratch fixture
this engine's own CHANGELOG has always verified changes against by hand;
this just automates and keeps them instead of throwing them away.
"""

import json
import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-traceability.sh"

DEFAULT_ID_RE = "(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?"
DEFAULT_COVERS_RE = "@covers[[:space:]]+.*"
DEFAULT_CARRIES_RE = r"\*\*(Carries|Traces)\*\*:"
DEFAULT_TEST_AC_RE = "AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?"


class Project:
    """A disposable fixture project rooted at tmp_path."""

    def __init__(self, root: Path):
        self.root = root
        (root / "specs" / "backlog").mkdir(parents=True, exist_ok=True)
        self._config = None

    def write(self, rel_path: str, content: str) -> Path:
        p = self.root / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return p

    def append(self, rel_path: str, content: str) -> Path:
        p = self.root / rel_path
        existing = p.read_text() if p.exists() else ""
        p.write_text(existing + content)
        return p

    def prd(self, *lines: str) -> Path:
        body = "\n".join(lines)
        return self.write("PRD.md", f"# Fixture PRD\n\n{body}\n")

    def raw_config(self, text: str) -> Path:
        """Write config.yml verbatim, bypassing the block-style builder --
        for fixtures that need to be malformed on purpose."""
        self._config = self.write("config.yml", text)
        return self._config

    def config(self, **overrides) -> Path:
        defaults = {
            "registry": "PRD.md",
            "target_name": "fixture",
            "manifest_path": "trace-manifest.json",
            "specs": "specs/**/spec.md",
            "tasks": "specs/**/tasks.md",
            "src_globs": ["src/**"],
            "test_globs": ["tests/**"],
        }
        defaults.update(overrides)
        lines = []
        for key, value in defaults.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                lines.extend(f'  - "{item}"' for item in value)
            elif isinstance(value, bool):
                lines.append(f"{key}: {'true' if value else 'false'}")
            else:
                lines.append(f'{key}: "{value}"')
        lines.append(f'id_regex: "{DEFAULT_ID_RE}"')
        lines.append(f'covers_regex: "{DEFAULT_COVERS_RE}"')
        lines.append(f'carries_regex: "{DEFAULT_CARRIES_RE}"')
        lines.append(f'test_ac_regex: "{DEFAULT_TEST_AC_RE}"')
        self._config = self.write("config.yml", "\n".join(lines) + "\n")
        return self._config

    def run(self, args=None):
        """Run the real script against this fixture; return (proc, manifest)."""
        assert self._config is not None, "call project.config() first"
        env = os.environ.copy()
        env["SPECASSAY_PROJECT_ROOT"] = str(self.root)
        env["SPECASSAY_CONFIG"] = str(self._config)
        proc = subprocess.run(
            ["bash", str(SCRIPT), *(args or [])],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        manifest_path = self.root / "trace-manifest.json"
        manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else None
        return proc, manifest

    def row(self, manifest: dict, id_: str) -> dict:
        for r in manifest["rows"]:
            if r["id"] == id_:
                return r
        raise AssertionError(f"{id_} not in manifest rows: {[r['id'] for r in manifest['rows']]}")


@pytest.fixture
def project(tmp_path) -> Project:
    return Project(tmp_path)
