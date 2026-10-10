# Staged skill updates awaiting install

- 2026-10-10/make-scenario-building — additive: step 5 (Connections) gets a
  check that the connection can see a new or externally created target
  (observation #4). Not packed as .skill: the bundle validator fails on
  Make's `{{now}}` syntax in examples/*.json (false positive, observation #6).
  Install: copy `2026-10-10/make-scenario-building/SKILL.md` over
  `.claude/skills/make-scenario-building/SKILL.md` (only that file differs).

- 2026-10-10/task-observer (+ task-observer.skill) — upstream refresh 3.5.0 →
  3.6.0 from github.com/rebelytics/one-skill-to-rule-them-all, commit
  56e890712273ce231b478adc56ee2eb81101c3d6 (CC BY 4.0). The local copy had no
  own edits. New: scripts/session-start-scan.sh and scripts/skill-load.sh;
  changes across SKILL.md and six reference files. Bundle gate passed.
  Install: replace `.claude/skills/task-observer/` with the staged directory.
