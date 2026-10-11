Source: https://github.com/bradautomates/claude-video (commit 03ceb42f7fa2c4439aca01752118044baabffb8f, v0.3.2), MIT.

Copied unchanged: `skills/watch/` (SKILL.md and scripts). Left out: the plugin's
SessionStart hook (`hooks/check-setup.sh`, an advisory check at every start), the
tests, the docs images and the plugin manifests; none of them is needed to run the skill.

Needs on the machine: Python 3.10+, ffmpeg/ffprobe, a current yt-dlp, and Deno for
YouTube. Works on the PC; in cloud sessions most video downloads are blocked, so
only local files are realistic there.
