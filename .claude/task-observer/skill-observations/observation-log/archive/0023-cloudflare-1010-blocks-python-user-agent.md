---
id: 23
title: "An API behind Cloudflare answered 403 'error code: 1010' to Python's default user agent while curl got through — looked like a bad key"
status: actioned
type: open-source
skill: [ai-music]
proposes_skill: []
target_file: []
siblings_checked: "none — no skill-families.md entry covers API-calling scripts; short-video-studio/stimme.py uses requests (own user agent), not checked for this"
area: "scripts/musik.py, HTTP request headers"
date: 2026-10-15
session_context: "Building the ai-music skill (acemusic.ai, ACE-Step 1.5) and testing it with a dummy key before the user has a real one"
parked_until:
resolved: 2026-10-15
resolution: "musik.py sends its own User-Agent header with a comment naming the 1010 block; the dummy-key test now reaches the API and gets the expected 401"
reference:
commands_verified: "run — curl POST without key: HTTP 401 auth_error; python urllib with dummy key: HTTP 403 'error code: 1010'; same call with a User-Agent header: HTTP 401 'Invalid or expired token'"
---

**Issue:** The new music script used `urllib` with no headers beyond auth. The
API returned `403 error code: 1010`, which the script reported as "key wrong or
expired". In fact Cloudflare in front of the API bans the default
`Python-urllib/x.y` user agent; curl (with its own UA) got the real 401. Without a
dummy-key test before the user creates an account, the user would have pasted a
valid key and seen a misleading "key invalid" error.

**Suggested improvement:** For any script calling a third-party HTTP API, set an
explicit `User-Agent`, and test once with a dummy key: the expected answer is the
service's own auth error, not a 403 from the edge.

**Principle:** Test an integration's failure path before the credential exists:
the error you get without a valid key must come from the service, not from the
network in front of it — otherwise the first real attempt blames the user's key.
