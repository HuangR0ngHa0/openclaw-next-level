---
name: jd-fit-analyzer
description: Analyze a job description against the user's real background, project history, and target direction. Use when the user wants to know whether a role fits, what strengths match, what gaps exist, whether the role is worth applying to, or how to adjust resume emphasis for robotics, autonomous driving, C++, ROS, Linux, OpenCV, embedded, and systems engineering roles.
---

# JD Fit Analyzer

Translate a JD into a concrete fit assessment for this user.

## Required references

- Read `skills/references/user-career-profile.md` before making conclusions.
- If a tailored resume already exists for the role, use it as supporting context, not as a substitute for the user's ground truth.

## Core workflow

1. Read the full JD content.
2. Extract the real requirement categories.
3. Compare them against the user's background.
4. Separate strengths, gaps, and packaging opportunities.
5. Decide whether the role is a strong target.

## Requirement categories

Use these buckets when possible:

- domain: robotics, autonomous driving, perception, localization, planning, control, embedded, tooling
- programming: C++, Python, algorithms, scripting
- platform: Linux, Ubuntu, ROS, ROS Noetic, build tools, debugging
- engineering: Git, testing, modularization, documentation, integration
- experience: internship, project ownership, team coordination, deployment
- education: degree, major, graduation status

## Hard rules

- Base conclusions on the JD and the user's actual profile.
- Do not invent experience the user does not have.
- Distinguish between true match, adjacent match, and clear gap.
- Prefer honest positioning over inflated claims.

## Output sections

Return these sections in order:

1. overall verdict
2. strong matches
3. partial matches / adjacent evidence
4. clear gaps
5. packaging opportunities
6. risk notes
7. application recommendation
8. resume adjustment hints
9. confidence note

## Packaging guidance for this user

Look for ways to frame experience as engineering evidence, for example:

- team lead / systems coordination in Formula Student driverless work
- perception, localization, planning, simulation, CAN, ROS-related work
- DLIO optimization as project-depth evidence
- OpenCV / embedded / robotics competition work as proof of execution

Do not convert competition work into fake corporate experience. Reframe honestly.
