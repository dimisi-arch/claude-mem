---
id: 15
title: "Short-form trend research without vidIQ credits: TikTok and Reels have no working fallback, YouTube Shorts has one (channel tabs via yt-dlp)"
status: actioned
type: open-source
skill: [agent-reach]
proposes_skill: []
target_file: []
siblings_checked: "none — no skill-families.md in this install; watch was considered: it watches one known video, it does not discover accounts (watch/SKILL.md description)"
area: "Platform coverage: TikTok account discovery and recent-post metrics"
date: 2026-10-13
session_context: "User asked for 5 viral faceless TikTok story accounts from the last 14 days plus a sample episode, then for the same comparison on Shorts and Reels; vidIQ outlier search had 0 credits (renews 2026-11-05)"
parked_until:
resolved: 2026-10-15
resolution: "Staged for agent-reach at skill-updates/2026-10-15/agent-reach (weekly review): Local-notes block on TikTok/Reels dead ends and the YouTube Shorts route, promoted with provenance (observed once, 2026-10-13, cloud)"
reference:
commands_verified: "run — vidiq_instagram_tiktok_outlier_search: 'Not enough credits'; curl/WebFetch tiktok.com/discover/*: redirect to homepage, no content; yt-dlp 2026.08.19 tiktok:tag 'CURRENTLY BROKEN', tiktok:user 'Failed to parse JSON' (no impersonate target); Playwright Chromium via HTTPS_PROXY on tiktok.com/search: login wall; Playwright on tiktok.com/@handle: /api/post/item_list answers 200 with an empty body, only profile totals (followers, likes, video count) in the page JSON; Playwright on /explore: puzzle captcha after the first load (not bypassed); curl on a single /@user/video/<id> page: playCount and createTime present (worked); Exa video URLs decoded by id>>32: newest from July 2026, none from the last 14 days; Exa web_search_exa with 'site:tiktok.com' yields @handles (153 from 16 queries, some calls fail on rate limit and need a sequential retry); YouTube: yt-dlp search with sp= sort/date filters returns mostly tiny new uploads (not usable for 'what is viral'), yt-dlp search with sp=EgIQAg%253D%253D (channels) returns subscriber counts (worked), yt-dlp --flat-playlist on /channel/<id>/shorts returns the newest Shorts with view_count but no date (worked, 64 of 78 channels), per-video yt-dlp date lookups hit HTTP 429 + 'confirm you are not a bot' after ~45 calls; TubeAlfred youtube_videos_batch gives publish_date but bills 1 credit per video and accepts only top-level field names (id,title,publish_date,view_count_int,channel,duration_ms); TubeAlfred youtube_search_query with type/sort/upload_date filters returned empty (4 credits spent)"
---

**Issue:** The only purpose-built tool for "what went viral on TikTok in the last N days" (vidIQ outlier search) ran out of credits. agent-reach lists 16 platforms but not TikTok, so the agent spent many calls finding a route: vendor blogs instead of accounts from WebSearch, TikTok discover/tag pages blocked from the cloud, yt-dlp's TikTok user/tag extractors broken, TikTok search behind a login. Every other route failed: profile video lists come back empty for a logged-out headless browser, /explore shows a puzzle captcha (bot detection, not to be bypassed), and the Exa index of TikTok video URLs lags months behind. Single video pages fetched with curl do carry plays and create time, and handles come from Exa `site:tiktok.com` queries — useful for checking known videos, useless for a 'last 14 days' question. Outcome: the request was answered with the creative half (sample episode) plus a scheduled re-run on the vidIQ credit reset date.

**Second instance (same session, YouTube Shorts):** asked to compare Shorts and Reels, the agent found a free route for Shorts only: channel discovery via yt-dlp channel search (subscriber counts), then each channel's /shorts tab (newest Shorts with views), then publish dates for a shortlist via a paid batch call because per-video lookups get rate-limited. Many large channels turned out inactive for months — a 'newest uploads' check is needed before calling any channel a current example. Reels: no logged-out route.

**Suggested improvement:** agent-reach: add a TikTok entry that states the dead ends up front (search/discover need login or redirect, tag/user extractors in yt-dlp broken, profile post lists empty logged out, explore captcha) and the two narrow things that work (Exa site:tiktok.com for handles, curl on a known video page for its stats). For recency questions the answer is: vidIQ, a logged-in session on the user's PC, or a scheduled re-run when credits reset — decide that in the first call, not after a dozen probes. Add a YouTube Shorts entry with the working three-step route (channel search → /shorts tab → batched dates for a shortlist only) and the warning that sort-by-views search filters and TubeAlfred search filters return noise or nothing.

**Principle:** When the paid data tool for a platform is exhausted, record per platform which questions the free routes can answer (known item: yes; 'what is trending now': no) in the research skill, so an exhausted quota leads straight to the honest options instead of a dozen probes; never treat a captcha as an obstacle to engineer around.
