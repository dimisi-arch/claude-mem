#!/bin/bash
# Fetch the remotion-best-practices skill (github.com/remotion-dev/skills) in
# cloud sessions. Its content is under the Remotion License, so it is not
# committed to this public repo: the folder is gitignored and downloaded here.
# Pinned to one commit; bump REV to update. Never fails the session start.

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

REV=6c67adcd9cdbe6eb84d76342da89b225f9161cb2   # skills version 4.0.538
DEST="$CLAUDE_PROJECT_DIR/.claude/skills/remotion-best-practices"
# Skip only when this exact REV is installed (.rev marker), so bumping REV refreshes it.
[ -f "$DEST/SKILL.md" ] && [ "$(cat "$DEST/.rev" 2>/dev/null)" = "$REV" ] && exit 0

tmp=$(mktemp -d)
if timeout 120 git -C "$tmp" init -q \
  && timeout 120 git -C "$tmp" fetch -q --depth 1 https://github.com/remotion-dev/skills "$REV" \
  && git -C "$tmp" checkout -q FETCH_HEAD \
  && [ -f "$tmp/skills/remotion-best-practices/SKILL.md" ]; then
  rm -rf "${DEST:?}" && cp -r "$tmp/skills/remotion-best-practices" "$DEST" && echo "$REV" > "$DEST/.rev"
  echo "remotion-best-practices skill installed" >&2
else
  echo "remotion-best-practices download failed; see .claude/hooks/install-remotion-skill.sh" >&2
fi
rm -rf "$tmp"
exit 0
