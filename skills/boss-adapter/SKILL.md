---
name: boss-adapter
description: Extract real job data from BOSS直聘 or similar job-listing pages as a source adapter for higher-level career skills. Use when a skill needs to collect job cards, enter detail pages, extract full JD text, and return structured role data without relying on list-page titles alone. Especially useful for shortlist building, JD collection, and filtering in Chinese job-market workflows.
---

# BOSS Adapter

Use BOSS as a source adapter, not as the main business workflow.

## Purpose

Collect structured job data for higher-level skills such as `job-intelligence`.

## Core workflow

1. Open or locate the BOSS listing page.
2. Collect candidate job cards from the current results view.
3. Enter detail pages when possible.
4. Extract full JD content and metadata.
5. Return normalized structured records.
6. Record failures by type.

## Hard rules

- Do not score or rank jobs here beyond basic adapter-level flags.
- Do not infer JD details from titles alone.
- Prefer detail-page extraction over list-page snippets.
- If detail-page access fails 3 times for the same item, stop and mark it as failed.
- If the page structure changes or anti-bot behavior appears, stop retrying aggressively and return partial results with failure notes.

## Extract these fields when available

- company
- role title
- city / district
- salary
- experience requirement
- education requirement
- responsibilities
- requirements
- tags / keywords
- benefits if visible
- source url
- retrieval timestamp
- extraction confidence

## Failure taxonomy

Use clear categories such as:

- detail-click-failed
- page-structure-changed
- login-required
- anti-bot-suspected
- jd-empty
- tab-lost

## Output contract

Return a list of records with:

- extracted fields
- source status: detail | list-only | failed
- failure reason if any
- confidence note

## Notes for this user's career workflow

This adapter should support downstream filtering for:

- Guangzhou / Shenzhen
- robotics / autonomous driving / C++ / ROS / Linux / systems roles
- junior or early-career engineering positions
