#!/bin/bash
# Fetch the HyperFrames skills (github.com/heygen-com/hyperframes, Apache 2.0)
# in cloud sessions: video from HTML, incl. a faceless-explainer workflow.
# Fetched instead of committed because the chosen set is ~6 MB; the folders
# sit in the gitignored .claude/skills/. Only the core set plus four creation
# workflows; the /hyperframes router installs other workflows on demand.
# Pinned to one commit; bump REV to update. Never fails the session start.

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

REV=f35b05fba0e8562b44a1edcf46ac2c1b79c1bca7   # tag v0.8.159 = npm hyperframes@0.8.159
SKILLS="hyperframes hyperframes-core hyperframes-cli hyperframes-animation
  hyperframes-creative hyperframes-audio hyperframes-keyframes
  hyperframes-registry hyperframes-studio media-use
  faceless-explainer general-video motion-graphics slideshow"
DIR="$CLAUDE_PROJECT_DIR/.claude/skills"

missing=0
# A skill counts as present only at this exact REV (.rev marker), so bumping REV refreshes all.
for s in $SKILLS; do [ -f "$DIR/$s/SKILL.md" ] && [ "$(cat "$DIR/$s/.rev" 2>/dev/null)" = "$REV" ] || missing=1; done
[ "$missing" = 0 ] && exit 0

paths=""
for s in $SKILLS; do paths="$paths skills/$s"; done

tmp=$(mktemp -d)
# Blob-less fetch + sparse checkout: downloads only the skill folders, not the 70 MB repo.
if timeout 120 git -C "$tmp" init -q \
  && git -C "$tmp" remote add origin https://github.com/heygen-com/hyperframes \
  && git -C "$tmp" sparse-checkout set --no-cone $paths LICENSE \
  && timeout 120 git -C "$tmp" fetch -q --depth 1 --filter=blob:none origin "$REV" \
  && timeout 120 git -C "$tmp" checkout -q FETCH_HEAD \
  && [ -f "$tmp/skills/hyperframes/SKILL.md" ]; then
  for s in $SKILLS; do
    [ -d "$tmp/skills/$s" ] || continue
    rm -rf "${DIR:?}/$s" && cp -r "$tmp/skills/$s" "$DIR/$s"
    cp "$tmp/LICENSE" "$DIR/$s/LICENSE.hyperframes"
    echo "$REV" > "$DIR/$s/.rev"
  done
  echo "HyperFrames skills installed" >&2
else
  echo "HyperFrames skills download failed; see .claude/hooks/install-hyperframes.sh" >&2
fi
rm -rf "$tmp"
exit 0
