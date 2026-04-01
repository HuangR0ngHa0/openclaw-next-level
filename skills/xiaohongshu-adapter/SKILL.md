---
name: xiaohongshu-adapter
description: Extract concrete content from Xiaohongshu as a source adapter for higher-level career and research skills. Use when a skill needs to search Xiaohongshu, inspect real posts, enter detail pages, and collect interview experience, company discussion, job-search tips, or technical discussion without relying on titles alone. Useful for interview-prep, company research, and social-signal gathering.
---

# Xiaohongshu Adapter

Use Xiaohongshu as a social signal source, not as the final decision-maker.

## Purpose

Collect verified post-level evidence for downstream skills such as `interview-prep-builder` and `job-intelligence`.

## Core workflow

1. Search with a concrete keyword or company-role query.
2. Parse result-page cards.
3. Enter detail pages when possible.
4. Validate that the detail page is real and readable.
5. Extract title, author, date, body, and engagement signals.
6. Return structured post records and failure notes.

## Hard rules

- Do not summarize from titles alone.
- Use detail-page validation before claiming success.
- If a detail page lacks real body content, mark it as failed or low-confidence.
- Stop retrying the same broken navigation path after 3 failures.
- If anti-automation behavior or unstable routing appears, return partial results and failure categories.

## Preferred extraction strategy

- Parse DOM from search results first.
- Prefer stable wrapper links when available.
- Fall back to alternate detail paths only when needed.
- Validate detail success using multiple signals such as title, author, body, comments, or engagement metadata.

## Useful fields

- query
- post title
- author
- date
- body summary
- notable claims
- company or role mention
- interview-related clues
- engagement metrics if visible
- source url
- confidence

## Failure taxonomy

Use categories such as:

- detail-open-failed
- unstable-routing
- body-missing
- login-wall
- anti-bot-suspected
- parse-failed

## Notes for this user's career workflow

Prioritize queries around:

- company name + 面经
- company name + 岗位
- 自动驾驶 面经
- 机器人 面经
- ROS / C++ / 自动驾驶 求职 discussion

Use Xiaohongshu as supporting evidence for:

- interview-prep-builder
- company research
- social-signal gathering

Do not treat Xiaohongshu commentary as hard fact; label rumor vs concrete firsthand detail.
