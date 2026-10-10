Source: https://github.com/pbakaus/impeccable (commit d631a8827f99414d2b6daba4ef08b7f8701751d7), skill 4.5.2, Apache License 2.0 (see LICENSE and NOTICE.md).

Copied unchanged: `plugin/skills/impeccable/` (SKILL.md, reference/, scripts/).
The launcher `scripts/impeccable` downloads its engine binary (v0.1.14, pinned in scripts/VERSION)
from the project's GitHub releases on first use and verifies it against the published .sha256
before running it. Tested 2026-10-10 in a cloud container: `engine-probe` and `detect` work.
Use: web pages, forms, dashboards (e.g. a future restaurant site or booking form) — not for videos.
