# Staged skill updates awaiting install

(2026-10-10: task-observer 3.6.0 and the make-scenario-building step-5 check were installed.)

- SUPERSEDED by 2026-10-23/install-third-party-skill — 2026-10-11/install-third-party-skill (+ .skill) — Step 4c "Skill needs a CLI
  tool", PATH check in Step 5, exception for narrowing an over-broad upstream
  description in Step 4a (observation #9). Gate passed.
- SUPERSEDED by 2026-10-15/documentation-and-adrs — 2026-10-11/documentation-and-adrs (+ .skill) — upstream refresh
  addyosmani/agent-skills 1401c8b → 1be8e34: new section "Prose Review" and
  one checklist line. Gate passed.
- SUPERSEDED by 2026-10-15/security-and-hardening — 2026-10-11/security-and-hardening (+ .skill) — upstream refresh, same
  commit: one zod example line in references/hardening-patterns.md. Gate passed.
- 2026-10-11/voice-summary (+ .skill) — NEW internal skill (observation #10,
  approved by the user 2026-10-11): spoken German summary → vorlesen.py
  --check → fix PRONUNCIATION → rerun → send. Gate passed.
  Install: `cp -r .claude/task-observer/skill-updates/2026-10-11/voice-summary .claude/skills/` and `git add -f`.

- 2026-10-15/agent-reach (+ .skill) — Local notes: short-form trend research
  without vidIQ credits (TikTok/Reels dead ends, YouTube Shorts route), with
  provenance (observation #15). Gate passed.
- SUPERSEDED by 2026-10-23 — 2026-10-15/ponytail-debt, ponytail-gain, ponytail (SOURCE only) (+ .skill) —
  upstream DietrichGebert/ponytail 9cc65d0 → 84740e3. Supersedes the 2026-10-13
  copies in unmerged PR #34. Gate passed.
- 2026-10-15/documentation-and-adrs, idea-refine, security-and-hardening (+ .skill)
  — upstream addyosmani/agent-skills 1401c8b → aeac41d (idea-refine is new in this
  round). Gate passed.
- SUPERSEDED by 2026-10-23/impeccable — 2026-10-15/impeccable (+ .skill) — upstream pbakaus/impeccable d631a88 → a231cc5:
  4 reference files; version 4.5.2 and engine 0.1.14 unchanged. Supersedes PR #34's copy. Gate passed.

- 2026-10-23/install-third-party-skill (+ .skill) — builds on the 2026-10-11 copy (#9) and adds:
  pin to the released tag for CLI-driven skills, size row in Step 3, .rev check + sparse
  checkout in Step 4b, REV-bump check in Step 5 (observations #18, #21). Gate passed.
- 2026-10-23/ponytail, ponytail-debt, ponytail-gain, ponytail-help (+ .skill) — upstream
  DietrichGebert/ponytail 9cc65d0 → 09c434a. Gate passed.
- 2026-10-23/impeccable (+ .skill) — upstream pbakaus/impeccable d631a88 → 4901415 (30 files). Gate passed.
- 2026-10-23/task-observer (+ .skill) — upstream rebelytics 3.6.0 → 3.7.0 (3463c7c, 68 commits);
  local copy was unchanged. Gate passed.
