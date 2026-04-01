---
name: interview-prep-builder
description: Build interview preparation packs for a specific company and role using the real JD, the user's background, and external discussion sources such as social posts, interview experience writeups, and community knowledge. Use when the user wants likely interview topics, project deep-dive questions, HR questions, company research notes, or a practical prep checklist for robotics, autonomous driving, C++, ROS, Linux, and engineering roles.
---

# Interview Prep Builder

Turn a JD into a realistic prep pack.

## Core workflow

1. Read the target JD.
2. Read the user's tailored resume or profile.
3. Search for interview experience, company discussion, and technical context.
4. Separate verified findings from weak signals.
5. Build a preparation checklist tied to the user's real projects.

## Research sources

Use a mix of:

- job detail pages
- company pages
- social/community discussion
- interview writeups
- technical community threads

Prefer sources with concrete detail over vague commentary.

## Hard rules

- Do not present rumors as facts.
- Label low-confidence findings clearly.
- Tie suggested answers back to the user's real experience.
- If company-specific evidence is missing, fall back to role-specific preparation.

## Prep pack structure

Return:

1. company and role snapshot
2. likely technical focus areas
3. likely project deep-dive questions
4. likely coding / engineering questions
5. likely HR / motivation questions
6. suggested answer angles based on the user's background
7. questions the user should ask the interviewer
8. last-minute revision checklist

## Focus areas for this user

Common high-value areas include:

- C++ fundamentals and engineering habits
- Linux / ROS / build and debug workflow
- perception, localization, planning, simulation, CAN communication
- trade-offs in robotics / autonomous systems design
- project ownership, team collaboration, integration, testing
- translating competition or student-team work into engineering impact

## Failure handling

If external interview data is sparse, say so explicitly and produce a role-based prep pack rather than pretending company-specific certainty.
