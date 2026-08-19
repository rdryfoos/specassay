# This repo's own Gate config

Claims registry IDs whose "build" is a change to `specassay-check-config.yml`
itself, once that change has actually shipped (real `@covers` mark, not an
anointment). Anointed backlog is for work not yet started; this spec is
where that same ID lands once it has.

- FR-DOCS-50 — `docs/**`, `README.md`, and `PROMOTION-CONTRACT.md` are back
  in `src_globs` (specassay-check-config.yml itself joined the list too, so
  the config's own `@covers` marks count). Shipped 2026-08-18 in the same
  pass as FR-GATE-40, which is what made restoring them safe.
