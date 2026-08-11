#!/usr/bin/env python3
"""Generate the v5 (beta) sample trace-manifests.

Two files, both exercising the v5 interop fields (tier / parents / origin /
rollup / emitter object; see docs/trace-manifest-v5.md):

  samples/sample-v5.trace-manifest.json
      "FieldKit" — a fictional field-data-collection app, SpecAssay-style:
      US/FR/NFR/AC dialect, registry-line origins, explicit parent edges and
      rollups. Deep enough to feel real (~34 rows across 7 domains).

  samples/clew-style-v5.trace-manifest.json
      A clew-flavored twin: ledger-minted IDs (no registry file), Swift code
      anchors with symbols, nativeStatus mapping. What an Ariadne-Thread emit
      could look like through the same glass.

Deterministic output (fixed timestamp) so re-runs don't churn the diff.
Rollups and counts are computed from the rows, never hand-maintained.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "samples"
STAMP = "2026-08-11T12:00:00Z"

TIER = {"US": "intent", "FR": "requirement", "NFR": "requirement", "AC": "criterion"}


def row(id_, statement, status, line, parents=(), impls=(), proofs=(), carries=(),
        native=None):
    kind = id_.split("-")[0]
    r = {
        "id": id_,
        "type": kind,
        "tier": TIER[kind],
        "statement": f"{id_} — {statement}",
        "origin": {"kind": "registry-line", "path": "PRD.md", "line": line},
        "registry": {"path": "PRD.md", "line": line},
        "status": status,
        "parents": list(parents),
        "implementations": [
            {"path": p, "line": ln, "excerpt": f"# @covers {id_}"} for (p, ln) in impls
        ],
        "proofs": [
            {"name": n, "path": p, "line": ln} for (n, p, ln) in proofs
        ],
        "carryingTasks": [
            {"path": p, "line": ln, "excerpt": ex} for (p, ln, ex) in carries
        ],
        "attestedBy": None,
    }
    if native:
        r["nativeStatus"] = native
    return r


def fieldkit_rows():
    R = []
    # ---- CAPT: offline capture (the happy, proven domain) ----
    R += [
        row("US-CAPT-01", "As a field tech, I record observations on site, connected or not.",
            "backlog", 12),
        row("FR-CAPT-01", "Observation forms render from a versioned template and validate locally.",
            "proven", 13, parents=["US-CAPT-01"],
            impls=[("src/capture/forms.py", 41)]),
        row("FR-CAPT-02", "Photos and GPS fixes attach to an observation as first-class fields.",
            "proven", 14, parents=["US-CAPT-01"],
            impls=[("src/capture/attachments.py", 22)]),
        row("AC-CAPT-01", "A completed form saves locally in under 1s with no network.",
            "proven", 15, parents=["FR-CAPT-01"],
            impls=[("src/capture/store.py", 18)],
            proofs=[("test_AC_CAPT_01_local_save_under_1s_offline", "tests/test_capture.py", 12)]),
        row("AC-CAPT-02", "Validation failures name the field and block save until fixed.",
            "proven", 16, parents=["FR-CAPT-01"],
            proofs=[("test_AC_CAPT_02_validation_names_field_blocks_save", "tests/test_capture.py", 33)]),
        row("AC-CAPT-03", "A photo attached offline is stored full-resolution and thumbnailed.",
            "proven", 17, parents=["FR-CAPT-02"],
            impls=[("src/capture/attachments.py", 57)],
            proofs=[("test_AC_CAPT_03_offline_photo_full_res_and_thumb", "tests/test_attachments.py", 9)]),
        row("AC-CAPT-04", "A GPS fix older than 30s is flagged stale on the form.",
            "tracked-debt", 18, parents=["FR-CAPT-02"],
            impls=[("src/capture/gps.py", 31)],
            carries=[("specs/capture/tasks.md", 21, "- [ ] T204 — Carries: AC-CAPT-04")]),
    ]
    # ---- SYNC: reconcile (proven with one owed proof) ----
    R += [
        row("US-SYNC-01", "As a field tech, my observations reach the team without me thinking about it.",
            "backlog", 22),
        row("FR-SYNC-01", "Queued observations sync in the background when a connection appears.",
            "proven", 23, parents=["US-SYNC-01"],
            impls=[("src/sync/queue.py", 15)]),
        row("AC-SYNC-01", "A queued observation appears on the team dashboard within 10s of reconnect.",
            "proven", 24, parents=["FR-SYNC-01"],
            impls=[("src/sync/queue.py", 62)],
            proofs=[("test_AC_SYNC_01_dashboard_within_10s_of_reconnect", "tests/test_sync.py", 14)]),
        row("AC-SYNC-02", "Sync retries with backoff and never drops an observation.",
            "proven", 25, parents=["FR-SYNC-01"],
            proofs=[("test_AC_SYNC_02_retry_backoff_never_drops", "tests/test_sync.py", 41)]),
        row("AC-SYNC-03", "Two techs editing the same observation merge without losing either edit.",
            "tracked-debt", 26, parents=["FR-SYNC-01"],
            impls=[("src/sync/merge.py", 28)],
            carries=[("specs/sync/tasks.md", 17, "- [ ] T311 — Carries: AC-SYNC-03")]),
    ]
    # ---- EXPORT: reports out ----
    R += [
        row("US-EXP-01", "As a project lead, I hand a client a report they can open anywhere.",
            "backlog", 30),
        row("FR-EXP-01", "Any filtered set of observations exports as PDF and CSV.",
            "proven", 31, parents=["US-EXP-01"],
            impls=[("src/export/report.py", 19)]),
        row("FR-EXP-02", "Exports embed the capture timestamps and GPS fixes verbatim.",
            "proven", 32, parents=["US-EXP-01"],
            impls=[("src/export/fields.py", 12)]),
        row("AC-EXP-01", "A 500-observation export completes in under 20s.",
            "proven", 33, parents=["FR-EXP-01"],
            proofs=[("test_AC_EXP_01_500_obs_under_20s", "tests/test_export.py", 22)]),
        row("AC-EXP-02", "The PDF renders every attached photo at print resolution.",
            "proven", 34, parents=["FR-EXP-01"],
            proofs=[("test_AC_EXP_02_pdf_photos_print_resolution", "tests/test_export.py", 48)]),
        row("AC-EXP-03", "CSV column order is stable across app versions.",
            "tracked-debt", 35, parents=["FR-EXP-02"],
            impls=[("src/export/fields.py", 44)],
            carries=[("specs/export/tasks.md", 9, "- [ ] T407 — Carries: AC-EXP-03")]),
    ]
    # ---- AUTH ----
    R += [
        row("US-AUTH-01", "As an org admin, only my team sees my project's data.",
            "backlog", 39),
        row("FR-AUTH-01", "Project access is role-scoped: admin, editor, viewer.",
            "proven", 40, parents=["US-AUTH-01"],
            impls=[("src/auth/roles.py", 16)]),
        row("AC-AUTH-01", "A viewer role cannot modify or export observations.",
            "proven", 41, parents=["FR-AUTH-01"],
            proofs=[("test_AC_AUTH_01_viewer_cannot_modify_or_export", "tests/test_auth.py", 11)]),
        row("AC-AUTH-02", "Revoking access takes effect on the revoked device within one sync.",
            "proven", 42, parents=["FR-AUTH-01"],
            proofs=[("test_AC_AUTH_02_revoke_effective_within_one_sync", "tests/test_auth.py", 37)]),
    ]
    # ---- PERF / A11Y: NFRs as parentless requirements ----
    R += [
        row("NFR-PERF-01", "The observation list stays at 60fps with 2,000 records on device.",
            "proven", 46,
            impls=[("src/ui/list_virtualizer.py", 8)],
            proofs=[("test_AC_PERF_01_list_60fps_2000_records", "tests/test_perf.py", 15)]),
        row("NFR-PERF-02", "Cold start to usable form in under 2s on a mid-range device.",
            "tracked-debt", 47,
            impls=[("src/app/boot.py", 5)],
            carries=[("specs/perf/tasks.md", 12, "- [ ] T512 — Carries: NFR-PERF-02")]),
        row("NFR-A11Y-01", "Every capture flow is operable by screen reader alone.",
            "proven", 48,
            impls=[("src/ui/a11y.py", 21)]),
        row("AC-A11Y-01", "Form fields announce label, value, and validation state.",
            "proven", 49, parents=["NFR-A11Y-01"],
            proofs=[("test_AC_A11Y_01_fields_announce_label_value_state", "tests/test_a11y.py", 10)]),
        row("AC-A11Y-02", "Photo capture is reachable and operable without touch gestures.",
            "backlog", 50, parents=["NFR-A11Y-01"],
            carries=[("specs/backlog/tasks.md", 14, "- [ ] T601 — Carries: AC-A11Y-02")]),
    ]
    # ---- MAPS: a minted-ahead domain, honestly blue ----
    R += [
        row("US-MAP-01", "As a project lead, I see every observation pinned on one map.",
            "backlog", 54),
        row("FR-MAP-01", "The map clusters pins and filters by the same query as the list.",
            "backlog", 55, parents=["US-MAP-01"]),
        row("AC-MAP-01", "Tapping a cluster zooms to its observations.",
            "backlog", 56, parents=["FR-MAP-01"]),
        row("AC-MAP-02", "Map view works from the offline tile cache.",
            "backlog", 57, parents=["FR-MAP-01"],
            carries=[("specs/backlog/tasks.md", 19, "- [ ] T702 — Carries: AC-MAP-02")]),
    ]
    return R


def add_rollups(rows):
    """Children from the declared edges; covered = all child criteria answered
    (proven or excused debt). Edges are canonical — this is the courtesy copy."""
    by_id = {r["id"]: r for r in rows}
    kids: dict[str, list[str]] = {}
    for r in rows:
        for p in r.get("parents", []):
            kids.setdefault(p, []).append(r["id"])
    ok = {"proven", "tracked-debt"}

    def covered(id_):
        ch = kids.get(id_, [])
        if not ch:
            return by_id[id_]["status"] in ok
        return all(covered(c) for c in ch)

    for id_, ch in kids.items():
        by_id[id_]["rollup"] = {
            "covered": covered(id_),
            "children": sorted(ch),
            "coveredChildren": sum(1 for c in ch if covered(c)),
        }


def manifest(emitter, target, repo, rows):
    counts = {"proven": 0, "tracked-debt": 0, "GAP": 0, "backlog": 0}
    for r in rows:
        counts[r["status"]] += 1
    crits = [r for r in rows if r["tier"] == "criterion"]
    return {
        "schemaVersion": 5,
        "format": "trace-manifest",
        "emitter": emitter,
        "targetName": target,
        "repoPath": repo,
        "generatedAt": STAMP,
        "gate": {"ok": True, "failures": []},
        "totals": {
            "registryIdCount": len(rows),
            "acCount": len(crits),
            "coveredCount": sum(1 for r in crits if r["status"] == "proven"),
        },
        "statusCounts": counts,
        "rows": rows,
    }


def clew_row(seq, id_, tier, statement, status, native, parents=(), impls=(), proofs=()):
    return {
        "id": id_,
        "type": "requirement" if tier == "requirement" else "acceptance-criterion",
        "tier": tier,
        "statement": statement,
        "origin": {"kind": "ledger", "ledger": ".clew/ledger", "seq": seq},
        "status": status,
        "nativeStatus": native,
        "parents": list(parents),
        "implementations": [
            {"path": p, "line": ln, "symbol": sym, "excerpt": f"// clew:{id_}"}
            for (p, ln, sym) in impls
        ],
        "proofs": [{"name": n, "path": p, "line": ln} for (n, p, ln) in proofs],
        "carryingTasks": [],
        "attestedBy": None,
    }


def clew_rows():
    R = [
        clew_row(41, "REQ-0041", "requirement",
                 "Observations captured offline reconcile across the team.",
                 "proven", "anchored"),
        clew_row(43, "CRIT-0043", "criterion",
                 "A change made offline appears on a second device within 2s of reconnect.",
                 "proven", "anchored", parents=["REQ-0041"],
                 impls=[("Sources/Sync/Reconcile.swift", 88, "reconcile")],
                 proofs=[("testReconcileWithinBudget", "Tests/SyncTests.swift", 40)]),
        clew_row(44, "CRIT-0044", "criterion",
                 "Concurrent disjoint edits merge without a conflict prompt.",
                 "proven", "anchored", parents=["REQ-0041"],
                 impls=[("Sources/Sync/Merge.swift", 31, "mergeDisjoint")],
                 proofs=[("testDisjointMergeSilent", "Tests/SyncTests.swift", 72)]),
        clew_row(52, "REQ-0052", "requirement",
                 "Every export carries its capture provenance.",
                 "tracked-debt", "partial"),
        clew_row(53, "CRIT-0053", "criterion",
                 "A PDF export embeds capture timestamp and device ID per observation.",
                 "proven", "anchored", parents=["REQ-0052"],
                 impls=[("Sources/Export/Provenance.swift", 19, "stampProvenance")],
                 proofs=[("testPdfEmbedsProvenance", "Tests/ExportTests.swift", 25)]),
        clew_row(54, "CRIT-0054", "criterion",
                 "A CSV export round-trips through re-import with provenance intact.",
                 "tracked-debt", "partial", parents=["REQ-0052"],
                 impls=[("Sources/Export/Csv.swift", 47, "writeCsv")]),
        clew_row(60, "REQ-0060", "requirement",
                 "Map view of all observations.",
                 "backlog", "pending"),
        clew_row(61, "CRIT-0061", "criterion",
                 "Pins cluster and zoom on tap.",
                 "backlog", "pending", parents=["REQ-0060"]),
    ]
    return R


def main():
    fk = fieldkit_rows()
    add_rollups(fk)
    m1 = manifest({"name": "specassay-check", "version": "0.9.0-beta"},
                  "FieldKit", "/work/fieldkit", fk)

    cr = clew_rows()
    add_rollups(cr)
    m2 = manifest({"name": "clew", "version": "0.9.0"},
                  "ariadne-demo", "/work/ariadne-demo", cr)
    m2["ext"] = {"clew": {"methodology": "CAS-DD", "ledgerHead": 61}}

    for name, m in [("sample-v5.trace-manifest.json", m1),
                    ("clew-style-v5.trace-manifest.json", m2)]:
        p = OUT / name
        p.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {p.relative_to(ROOT)}  rows={len(m['rows'])}  "
              f"statusCounts={m['statusCounts']}")


if __name__ == "__main__":
    main()
