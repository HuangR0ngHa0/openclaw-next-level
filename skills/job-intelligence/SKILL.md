---
name: job-intelligence
description: Discover, filter, and extract job opportunities for the user from recruitment sites and company career pages. Use when the user wants to find suitable jobs, screen positions, collect real JD details from detail pages, compare openings, or build a shortlist for applications in cities such as Guangzhou and Shenzhen. Especially useful for robotics, autonomous driving, embedded, systems, C++, ROS, Linux, perception, localization, planning, and related engineering roles.
---

# Job Intelligence

Build a reliable shortlist of roles instead of dumping search results.

## Core workflow

1. Read the user's target city, role direction, experience level, and constraints.
2. Search one or more job sources.
3. Enter detail pages when possible; do not infer from titles alone.
4. Extract the real JD text and key metadata.
5. Filter out low-quality roles.
6. Rank the remaining roles and summarize why they fit.

## Hard rules

- Prefer detail-page content over list-page snippets.
- Do not guess missing JD details.
- If detail-page access fails repeatedly, report the failure and continue with other jobs or sources.
- Stop retrying the same fragile action after 3 failures.
- Flag uncertainty explicitly.

## Extraction targets

Capture, when available:

- company
- job title
- city
- salary range
- experience requirement
- education requirement
- tech stack keywords
- job responsibilities
- qualification requirements
- source URL
- retrieval time

## Recommended filtering rules for this user

Prioritize:

- Guangzhou / Shenzhen
- autonomous driving / robotics / intelligent systems
- C++, Python, Linux, ROS, OpenCV, perception, localization, planning, control, embedded, CAN, tooling
- intern / campus / junior engineering roles with growth potential

Down-rank or reject:

- training / outsourcing traps
- fake technical roles that are mostly sales or support
- roles that require several years of formal full-time experience with no flexibility
- roles far outside the user's target cities unless explicitly requested

## Output format

For each kept role, return:

- fit summary
- extracted JD highlights
- likely strengths match
- likely gaps
- recommendation: apply / maybe / skip
- confidence and failure notes

## Notes

Treat each website as a data source adapter, not as the main business logic.
Keep source-specific logic minimal and reusable.
