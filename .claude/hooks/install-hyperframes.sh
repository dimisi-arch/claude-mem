#!/bin/bash
# Fetch the HyperFrames skills (github.com/heygen-com/hyperframes, Apache 2.0)
# in cloud sessions: video from HTML (explainers, motion graphics, maps, decks).
# Fetched instead of committed because the chosen set is ~6 MB; the folders
# sit in the gitignored .claude/skills/. Only the set below; the /hyperframes router
# installs other skills on demand.
# Pinned to one commit; bump REV to update. Never fails the session start.

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

REV=bbf9f8ffd0b2faa5edca9852c5528c5312f6c57e   # tag v0.8.186 = npm hyperframes@0.8.186
# Since v0.8.17x upstream folds the workflows (explainer, motion graphics, general video, ...)
# into hyperframes/references/types; the old per-workflow skills no longer exist.
SKILLS="hyperframes hyperframes-cli hyperframes-registry media-use slideshow remotion-to-hyperframes"
DIR="$CLAUDE_PROJECT_DIR/.claude/skills"

# Remove HyperFrames skills an older REV installed that are no longer in the set.
for d in "$DIR"/*/; do
  [ -f "$d/LICENSE.hyperframes" ] || continue
  case " $(echo $SKILLS) " in *" $(basename "$d") "*) ;; *) rm -rf "${d:?}" ;; esac
done

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
