---
id: 13
title: "TikTok trend research has no working fallback when vidIQ credits are gone: every logged-out route is blocked or stale"
status: open
type: open-source
skill: [agent-reach]
proposes_skill: []
target_file: []
siblings_checked: "none — no skill-families.md in this install; watch was considered: it watches one known video, it does not discover accounts (watch/SKILL.md description)"
area: "Platform coverage: TikTok account discovery and recent-post metrics"
date: 2026-10-13
session_context: "User asked for 5 viral faceless TikTok story accounts from the last 14 days plus a sample episode; vidIQ outlier search had 0 credits (renews 2026-11-05)"
parked_until:
resolved:
resolution:
reference:
commands_verified: "run — vidiq_instagram_tiktok_outlier_search: 'Not enough credits'; curl/WebFetch tiktok.com/discover/*: redirect to homepage, no content; yt-dlp 2026.08.19 tiktok:tag 'CURRENTLY BROKEN', tiktok:user 'Failed to parse JSON' (no impersonate target); Playwright Chromium via HTTPS_PROXY on tiktok.com/search: login wall; Playwright on tiktok.com/@handle: /api/post/item_list answers 200 with an empty body, only profile totals (followers, likes, video count) in the page JSON; Playwright on /explore: puzzle captcha after the first load (not bypassed); curl on a single /@user/video/<id> page: playCount and createTime present (worked); Exa video URLs decoded by id>>32: newest from July 2026, none from the last 14 days; Exa web_search_exa with 'site:tiktok.com' yields @handles (153 from 16 queries, some calls fail on rate limit and need a sequential retry)"
---

**Issue:** The only purpose-built tool for "what went viral on TikTok in the last N days" (vidIQ outlier search) ran out of credits. agent-reach lists 16 platforms but not TikTok, so the agent spent many calls finding a route: vendor blogs instead of accounts from WebSearch, TikTok discover/tag pages blocked from the cloud, yt-dlp's TikTok user/tag extractors broken, TikTok search behind a login. Every other route failed: profile video lists come back empty for a logged-out headless browser, /explore shows a puzzle captcha (bot detection, not to be bypassed), and the Exa index of TikTok video URLs lags months behind. Single video pages fetched with curl do carry plays and create time, and handles come from Exa `site:tiktok.com` queries — useful for checking known videos, useless for a 'last 14 days' question. Outcome: the request was answered with the creative half (sample episode) plus a scheduled re-run on the vidIQ credit reset date.

**Suggested improvement:** agent-reach: add a TikTok entry that states the dead ends up front (search/discover need login or redirect, tag/user extractors in yt-dlp broken, profile post lists empty logged out, explore captcha) and the two narrow things that work (Exa site:tiktok.com for handles, curl on a known video page for its stats). For recency questions the answer is: vidIQ, a logged-in session on the user's PC, or a scheduled re-run when credits reset — decide that in the first call, not after a dozen probes.

**Principle:** When the paid data tool for a platform is exhausted, record per platform which questions the free routes can answer (known item: yes; 'what is trending now': no) in the research skill, so an exhausted quota leads straight to the honest options instead of a dozen probes; never treat a captcha as an obstacle to engineer around.
