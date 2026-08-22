#!/usr/bin/env python3
"""specassay dig -- archaeology mode, the no-LLM floor.

Per docs/archaeology-mode-build-handoff-v1-2026-08-20.md (rung (a) of the
three-rung ladder; rungs (b) local-model and (c) user-supplied-API-key are
out of scope for this build). Static heuristics over an unfamiliar,
undocumented repo's own test names, routes, structure, prose, and commit
history propose a first-pass candidate registry -- a starting map for a
stranger dropped into someone else's codebase, not a minted one.

THE ONE HARD LAW: no dug row is ever written into a real registry, ever, by
this command. `dig` only ever produces `dig-report.json` -- flat data, never
loaded by the Gate, never chained, never covering or gating anything. Every
row carries epistemicClass="inferred" (constant, always present). There is
no --anoint flag here; turning a proposed row into a real, dated, minted
registry row is separate, later, human work.

Sources, in priority order (highest-signal first, per handoff Sec.3):
  1. Test names/bodies      -> candidate AC statements (provenance: test file:line)
  2. Routes / API surface   -> candidate FR statements (provenance: declaring file:line)
  3. Module/directory structure -> not its own rows; an area lookup used to
     annotate every other row's suggestedArea
  4. README/docs prose      -> candidate US statements (lowest priority,
     highest paraphrase risk -- short excerpts only)
  5. Commit history         -> stratigraphy/grouping signal attached per row
     (recentActivity), never used to mint a row on its own

Zero dependencies (stdlib only). Reads nothing but the target repo's own
files; writes nothing but dig-report.json (or wherever --out points).

Usage:
  dig.py [path] [--out PATH] [--sources tests,routes,structure,readme,commits]
         [--dry-run]

  path defaults to the current directory. --sources defaults to "all".
  --dry-run prints what would be written (counts by type and source) and
  writes nothing at all, not even a partial file.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

GENERATOR_VERSION = "0.2.0"  # level two: candidateProof, table mining, splitter fix, known-smoke labeling
EPISTEMIC_CLASS = "inferred"  # constant, always present, never omitted -- @covers FR-DIG-20

ALL_SOURCES = ("tests", "routes", "structure", "readme", "commits")

# Directories never treated as source: never worth digging, and would drown
# real signal in vendored/generated noise.
SKIP_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "vendor", "target", "build",
    "dist", "out", ".idea", ".vscode", ".gradle", ".mvn", "__pycache__",
    ".pytest_cache", ".specify", "coverage", ".venv", "venv",
}


def iter_files(root: Path, suffixes: tuple[str, ...]) -> list[Path]:
    out = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts[:-1]):
            continue
        if p.suffix in suffixes:
            out.append(p)
    return sorted(out)


def humanize(name: str) -> str:
    """test_user_can_retire_a_policy -> "user can retire a policy".

    camelCase-splitting only applies when the name has no underscores at
    all (a pure camelCase/PascalCase name, e.g. Go's TestUserCanRetire) --
    running it on an already-snake_case name mangles embedded acronyms and
    digit runs (test_AC_A11Y_01_... -> "a11" + "y", a real bug caught
    dogfooding this against this repo's own tests before shipping).

    Two splitting rules, applied in order, within that camelCase-only
    branch:
    1. An acronym/single-capital boundary before a real word -- an
       uppercase letter immediately followed by another uppercase+lowercase
       pair splits before the second uppercase (HTTPServer -> HTTP Server;
       issuesAPolicy -> issues A Policy). Level-two fix (dig-level-two
       handoff Sec.2b): without it, a lone capitalized article butting a
       capitalized word never split (bindingFromTheViewIssuesAPolicy ->
       "...issues apolicy", WithoutAFiledRate -> "...without afiled rate"),
       caught in the insurance-java honest-usefulness assessment.
    2. The ordinary lowercase/digit-to-uppercase boundary (already shipped).
    """
    name = re.sub(r"^(test_|test)", "", name, flags=re.IGNORECASE)
    if "_" not in name and "-" not in name:
        name = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", name)
        name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    words = [w for w in re.split(r"[_\-]+", name) if w]
    return " ".join(w.lower() for w in words)


# Full-line comment prefixes, by suffix -- a comment can legitimately
# contain example code (a doc explaining what a pattern matches, say) that
# must not be mined as if it were real code. Same mention-vs-use problem
# check-traceability.sh's own strip_code_spans()/is_local_domain() solve for
# the Gate (FR-GATE-40); this is the same fix for this tool's own scanners.
# Line-start only, not inline trailing comments (simpler, and inline
# stripping risks corrupting a route/test string that legitimately contains
# "#" or "//").
COMMENT_PREFIX = {".py": "#", ".java": "//", ".js": "//", ".ts": "//", ".go": "//"}


def is_comment_line(line: str, suffix: str) -> bool:
    prefix = COMMENT_PREFIX.get(suffix)
    return bool(prefix) and line.strip().startswith(prefix)


# ---------- 1. Test names/bodies -> candidate AC statements ----------

# Known-smoke noise (dig-level-two handoff Sec.2c): a small, NAMED list of
# recognized framework-smoke-test shapes, not a fuzzy semantic classifier.
# Never dropped -- every found test still becomes a row -- but pre-labeled
# low-confidence with a stated reason, so an anointment reviewer's
# two-second toss is already explained rather than something they have to
# work out themselves each time. contextLoads is Spring Boot's own default
# generated test; the insurance-java run is what surfaced it as real noise.
# @covers FR-DIG-50, AC-DIG-50
KNOWN_SMOKE_TESTS = {"contextloads", "smoketest", "smoke_test", "smoke"}


def is_known_smoke_test(raw_name: str) -> bool:
    bare = re.sub(r"^(test_|test)", "", raw_name, flags=re.IGNORECASE).lower()
    bare = bare.replace("_", "")
    return bare in KNOWN_SMOKE_TESTS


TEST_PATTERNS = [
    # Python: def test_xxx(
    (".py", re.compile(r"^\s*def\s+(test_\w+)\s*\(")),
    # Java/JUnit: a @Test-annotated method, name on the same or a following line
    (".java", re.compile(r"^\s*(?:public|private|protected)?\s*void\s+(\w+)\s*\(")),
    # JS/TS: it('...') / test('...')
    (".js", re.compile(r"""\b(?:it|test)\(\s*['"`](.+?)['"`]""")),
    (".ts", re.compile(r"""\b(?:it|test)\(\s*['"`](.+?)['"`]""")),
    # Go: func TestXxx(
    (".go", re.compile(r"^\s*func\s+(Test\w+)\s*\(")),
]


def dig_tests(root: Path) -> list[dict]:
    rows = []
    by_suffix: dict[str, list[re.Pattern]] = {}
    for suf, pat in TEST_PATTERNS:
        by_suffix.setdefault(suf, []).append(pat)

    for suf, patterns in by_suffix.items():
        for f in iter_files(root, (suf,)):
            try:
                lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            java_pending_test = False
            for i, line in enumerate(lines, start=1):
                if is_comment_line(line, suf):
                    continue
                if suf == ".java" and "@Test" in line:
                    java_pending_test = True
                    continue
                for pat in patterns:
                    m = pat.search(line)
                    if not m:
                        continue
                    if suf == ".java" and not java_pending_test:
                        continue
                    java_pending_test = False
                    raw_name = m.group(1)
                    statement = humanize(raw_name) or raw_name
                    row = {
                        "type": "AC",
                        "statement": statement,
                        "epistemicClass": EPISTEMIC_CLASS,
                        "confidence": "high",
                        "provenance": {
                            "source": "test",
                            "file": str(f.relative_to(root)),
                            "line": i,
                            "testName": raw_name,
                        },
                    }
                    if is_known_smoke_test(raw_name):
                        row["confidence"] = "low"
                        row["confidenceReason"] = "framework smoke test"
                    rows.append(row)
    return rows


# ---------- 2. Routes / API surface -> candidate FR statements ----------

ROUTE_PATTERNS = [
    # Spring: @GetMapping("/x"), @PostMapping(value="/x"), @RequestMapping(...)
    (".java", re.compile(
        r'@(Get|Post|Put|Delete|Patch|Request)Mapping\s*\(\s*(?:value\s*=\s*)?["\']([^"\']+)["\']'
    )),
    # Flask: @app.route("/x")
    (".py", re.compile(r'@\w+\.route\(\s*["\']([^"\']+)["\']')),
    # Express: app.get('/x', ...) / router.post('/x', ...)
    (".js", re.compile(r'\b\w+\.(get|post|put|delete|patch)\(\s*[\'"]([^\'"]+)[\'"]')),
    (".ts", re.compile(r'\b\w+\.(get|post|put|delete|patch)\(\s*[\'"]([^\'"]+)[\'"]')),
]


def dig_routes(root: Path) -> list[dict]:
    rows = []
    for suf, pat in ROUTE_PATTERNS:
        for f in iter_files(root, (suf,)):
            try:
                lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines, start=1):
                if is_comment_line(line, suf):
                    continue
                for m in pat.finditer(line):
                    groups = m.groups()
                    method = groups[0].upper() if len(groups) > 1 else ""
                    path = groups[-1]
                    statement = f"the system accepts {method} {path}".strip() if method else f"the system accepts {path}"
                    rows.append({
                        "type": "FR",
                        "statement": statement,
                        "epistemicClass": EPISTEMIC_CLASS,
                        "confidence": "high",
                        "provenance": {
                            "source": "route",
                            "file": str(f.relative_to(root)),
                            "line": i,
                        },
                    })
    return rows


# ---------- 3. Module/directory structure -> area lookup (not rows) ----------

def dig_structure(root: Path) -> dict[str, str]:
    """Top-level source directories as candidate AREA names. Returns a map
    from a leading path segment to a suggested area name, used to annotate
    every other row -- not emitted as rows of its own."""
    areas: dict[str, str] = {}
    common_roots = [root, root / "src" / "main" / "java", root / "src", root / "lib", root / "app"]
    for base in common_roots:
        if not base.is_dir():
            continue
        for child in sorted(base.iterdir()):
            if not child.is_dir() or child.name in SKIP_DIRS or child.name.startswith("."):
                continue
            try:
                rel = child.relative_to(root)
            except ValueError:
                continue
            areas[str(rel)] = child.name.upper()
    return areas


def area_for(path: str, areas: dict[str, str]) -> str | None:
    best = None
    for prefix, area in areas.items():
        if path.startswith(prefix) and (best is None or len(prefix) > len(best[0])):
            best = (prefix, area)
    return best[1] if best else None


# ---------- 4. README/docs prose -> candidate US statements ----------

HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$")


def dig_readme(root: Path) -> list[dict]:
    rows = []
    candidates = []
    for name in ("README.md", "README.rst", "README.txt"):
        p = root / name
        if p.is_file():
            candidates.append(p)
    docs_dir = root / "docs"
    if docs_dir.is_dir():
        candidates.extend(sorted(docs_dir.glob("*.md"))[:10])  # bounded, not a full crawl

    for f in candidates:
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, start=1):
            m = HEADING_RE.match(line)
            if not m:
                continue
            heading = m.group(2).strip()
            if len(heading) < 3 or len(heading) > 120:
                continue
            # Short excerpt only -- copyright discipline, no long reproduction.
            rows.append({
                "type": "US",
                "statement": heading[:120],
                "epistemicClass": EPISTEMIC_CLASS,
                "confidence": "low",
                "provenance": {
                    "source": "readme",
                    "file": str(f.relative_to(root)),
                    "line": i,
                },
                "candidateProof": None,
            })
    return rows


# ---------- 4b. README/docs markdown TABLE mining (level two, Sec.2a) ----------
#
# The found gap: heading-only mining missed the richest signal a project can
# offer -- a hand-maintained Spec -> Scenario -> Test coverage table sitting
# in plain markdown. A column whose header names it as "spec"/"scenario"/
# "test" (case-insensitive substring match, not an exact vocabulary) yields
# US/AC candidates and, when a test column is present, a "matched"
# candidateProof -- an inferred pairing from table structure, distinct from
# "same-artifact" (the test heuristic's own provenance doubling as proof).

TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
CODE_SPAN_RE = re.compile(r"^`([^`]+)`$")


def split_table_row(line: str) -> list[str]:
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", inner)]


def strip_code_span(s: str) -> str:
    m = CODE_SPAN_RE.match(s.strip())
    return m.group(1) if m else s.strip()


def split_scenarios(cell: str) -> list[str]:
    return [p.strip() for p in re.split(r"\s*[·;]\s*", cell) if p.strip()]


def find_test_declaration(root: Path, token: str) -> tuple[str | None, int | None]:
    """Resolve a bare test-class/function token (from a table's Test column)
    to a real file:line if one exists under root, so a table-matched
    candidateProof is actually actionable, not just a name.

    Searches file CONTENTS for a declaration, not just filename stems --
    a Java-style one-class-per-file convention (the table's Test column
    naming a file that also happens to share its stem) is common, but a
    Python/JS/Go test token is often a function inside a file shared by
    many tests, where filename-stem matching finds nothing at all (a real
    bug caught building the table-mining acceptance test against a
    Python-shaped fixture)."""
    token = strip_code_span(token)
    decl_re = re.compile(rf"\b(?:class|def|func)\s+{re.escape(token)}\b")
    stem_match: tuple[str, int] | None = None
    for suf in (".java", ".py", ".js", ".ts", ".go"):
        for f in iter_files(root, (suf,)):
            try:
                lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines, start=1):
                if decl_re.search(line):
                    return str(f.relative_to(root)), i
            if f.stem == token and stem_match is None:
                stem_match = (str(f.relative_to(root)), 1)
    if stem_match:
        return stem_match
    return None, None


def dig_readme_tables(root: Path) -> list[dict]:
    # @covers FR-DIG-30, AC-DIG-60, AC-DIG-40
    rows: list[dict] = []
    candidates = []
    for name in ("README.md", "README.rst", "README.txt"):
        p = root / name
        if p.is_file():
            candidates.append(p)
    docs_dir = root / "docs"
    if docs_dir.is_dir():
        candidates.extend(sorted(docs_dir.glob("*.md"))[:10])

    for f in candidates:
        if f.suffix != ".md":
            continue  # table syntax is a markdown convention
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        n = len(lines)
        i = 0
        while i < n - 1:
            if not TABLE_ROW_RE.match(lines[i]) or not TABLE_SEP_RE.match(lines[i + 1]):
                i += 1
                continue
            header_cells = split_table_row(lines[i])
            header_lower = [h.lower() for h in header_cells]
            spec_idx = next((k for k, h in enumerate(header_lower) if "spec" in h), None)
            scenario_idx = next((k for k, h in enumerate(header_lower) if "scenario" in h), None)
            test_idx = next((k for k, h in enumerate(header_lower) if "test" in h), None)
            if spec_idx is None and scenario_idx is None:
                i += 1
                continue  # not a spec-coverage-shaped table
            j = i + 2
            while j < n and TABLE_ROW_RE.match(lines[j]):
                cells = split_table_row(lines[j])
                needed = max((idx for idx in (spec_idx, scenario_idx, test_idx) if idx is not None), default=-1)
                if len(cells) <= needed:
                    j += 1
                    continue
                test_token = None
                test_file = test_line = None
                if test_idx is not None and cells[test_idx]:
                    test_token = strip_code_span(cells[test_idx])
                    test_file, test_line = find_test_declaration(root, test_token)

                if spec_idx is not None and cells[spec_idx]:
                    rows.append({
                        "type": "US",
                        "statement": cells[spec_idx],
                        "epistemicClass": EPISTEMIC_CLASS,
                        "confidence": "high",
                        "provenance": {"source": "readme-table", "file": str(f.relative_to(root)), "line": j + 1},
                        "candidateProof": None,
                    })
                if scenario_idx is not None and cells[scenario_idx]:
                    for scenario in split_scenarios(cells[scenario_idx]):
                        row = {
                            "type": "AC",
                            "statement": scenario,
                            "epistemicClass": EPISTEMIC_CLASS,
                            "confidence": "high",
                            "provenance": {"source": "readme-table", "file": str(f.relative_to(root)), "line": j + 1},
                            "candidateProof": None,
                        }
                        if test_token:
                            row["candidateProof"] = {
                                "test": test_token,
                                "file": test_file,
                                "line": test_line,
                                "basis": "matched",
                            }
                        rows.append(row)
                j += 1
            i = j
    return rows


# ---------- 5. Commit history -> stratigraphy signal, attached per row ----------

def recent_activity(root: Path, rel_path: str, limit: int = 3) -> list[dict]:
    """Up to `limit` most recent commits touching this file. Grouping/
    stratigraphy signal only -- never used to mint a row on its own."""
    try:
        proc = subprocess.run(
            ["git", "log", f"-n{limit}", "--follow", "--format=%h|%ad|%s", "--date=short", "--", rel_path],
            cwd=root, capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if proc.returncode != 0:
        return []
    out = []
    for line in proc.stdout.splitlines():
        parts = line.split("|", 2)
        if len(parts) != 3:
            continue
        h, date, subject = parts
        out.append({"commit": h, "date": date, "subject": subject})
    return out


def is_git_repo(root: Path) -> bool:
    return (root / ".git").exists()


# ---------- assembly ----------

def attach_candidate_proof(rows: list[dict]) -> None:
    """@covers FR-DIG-40 -- candidateProof is first-class on every row, not
    a viewer's inference from provenance.source == "test". Table mining
    already sets its own ("matched", possibly with a resolved file:line);
    this only fills the remaining case: a test-heuristic row's own
    provenance test IS its candidate proof ("same-artifact"). Every other
    row keeps candidateProof: null -- honest absence, not a guess."""
    for row in rows:
        row.setdefault("candidateProof", None)
        if row["candidateProof"] is None and row["provenance"]["source"] == "test":
            row["candidateProof"] = {
                "test": row["provenance"]["testName"],
                "file": row["provenance"]["file"],
                "line": row["provenance"]["line"],
                "basis": "same-artifact",
            }


def build_report(root: Path, sources: list[str]) -> dict:
    rows: list[dict] = []
    if "tests" in sources:
        rows += dig_tests(root)
    if "routes" in sources:
        rows += dig_routes(root)
    areas = dig_structure(root) if "structure" in sources else {}
    if "readme" in sources:
        rows += dig_readme(root)
        rows += dig_readme_tables(root)

    attach_candidate_proof(rows)

    for row in rows:
        row["suggestedArea"] = area_for(row["provenance"]["file"], areas) if areas else None

    if "commits" in sources and is_git_repo(root):
        for row in rows:
            row["recentActivity"] = recent_activity(root, row["provenance"]["file"])

    source_commit = None
    if is_git_repo(root):
        try:
            proc = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, timeout=10,
            )
            if proc.returncode == 0:
                source_commit = proc.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass

    return {
        "format": "dig-report",
        "generatorVersion": GENERATOR_VERSION,
        "sourceRepoPath": str(root),
        "sourceCommit": source_commit,
        "generatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="specassay dig -- archaeology mode, no-LLM floor")
    parser.add_argument("path", nargs="?", default=".", help="Target repo path (default: cwd)")
    parser.add_argument("--out", default=None, help="Output path (default: dig-report.json in the CURRENT WORKING DIRECTORY, not the target path -- durable and under the operator's own control even when the target isn't, e.g. a read-only clone of someone else's repo)")
    parser.add_argument("--sources", default="all", help="Comma-separated source list (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Print counts, write nothing")
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"dig: not a directory: {root}", file=sys.stderr)
        return 2

    sources = list(ALL_SOURCES) if args.sources == "all" else [s.strip() for s in args.sources.split(",") if s.strip()]
    unknown = set(sources) - set(ALL_SOURCES)
    if unknown:
        print(f"dig: unknown source(s): {', '.join(sorted(unknown))} (known: {', '.join(ALL_SOURCES)})", file=sys.stderr)
        return 2

    report = build_report(root, sources)
    # @covers FR-DIG-10, AC-DIG-30 -- default output is CWD-relative, never
    # target-relative: a stranger's repo (§0 of the build handoff -- cloned
    # read-only, never written to) and a session-scratch working directory
    # are both places a report must not default into, since either one can
    # vanish or get cleaned up out from under a claim that cites it. The
    # operator's own cwd is the one location guaranteed durable and under
    # their control regardless of what --path points at.
    out_path = Path(args.out).resolve() if args.out else Path.cwd() / "dig-report.json"

    by_type: dict[str, int] = {}
    by_source: dict[str, int] = {}
    for row in report["rows"]:
        by_type[row["type"]] = by_type.get(row["type"], 0) + 1
        src = row["provenance"]["source"]
        by_source[src] = by_source.get(src, 0) + 1

    # @covers FR-DIG-10, AC-DIG-10, AC-DIG-20 -- dry-run prints the same
    # counts a real run would and returns before touching the filesystem at
    # all; no partial file, no exception path that could leave one behind.
    if args.dry_run:
        print(f"dig: dry run -- would write {len(report['rows'])} candidate rows to {out_path}")
        print(f"  by type: {by_type}")
        print(f"  by source: {by_source}")
        print("dig: dry run -- nothing written")
        return 0

    # @covers FR-DIG-10, AC-DIG-10 -- the only write this command ever makes:
    # out_path itself. No other file on disk is ever opened for writing.
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"dig: wrote {out_path} ({len(report['rows'])} candidate rows)")
    print(f"  by type: {by_type}")
    print(f"  by source: {by_source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
