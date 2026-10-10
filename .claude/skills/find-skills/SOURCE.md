Source: https://github.com/vercel-labs/skills (commit 13e4063a1cf913f5606d57d42ab83a86f5001e04), `skills/find-skills/SKILL.md`, MIT License (see LICENSE).

Changed: an added "Local notes" block — search only with `npx skills find`, never `npx skills add`;
installs go through `install-third-party-skill`; warning about copied skills with inflated install counts.
Not installed: the `skills` CLI itself — `npx -y skills find` downloads it on demand (tested in a cloud container).
