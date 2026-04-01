---
name: career-pipeline
description: Orchestrate the full job-application workflow for the user: discover suitable roles, extract real JDs, analyze fit, tailor resumes, and build interview preparation packs. Use when the user wants an end-to-end career automation flow rather than a single isolated step, especially for Guangzhou / Shenzhen robotics, autonomous driving, C++, ROS, Linux, embedded, and related engineering roles.
---

# Career Pipeline

Coordinate the full job-search and application-preparation flow.

## Required references and component skills

Read or use these in the appropriate order:

- `skills/references/user-career-profile.md`
- `skills/references/resume-master.md`
- `skills/references/first-drill-template.md` when running the first end-to-end validation
- `skills/job-intelligence/SKILL.md`
- `skills/jd-fit-analyzer/SKILL.md`
- `skills/resume-tailor/SKILL.md`
- `skills/interview-prep-builder/SKILL.md`
- source adapters such as `skills/boss-adapter/SKILL.md` and `skills/xiaohongshu-adapter/SKILL.md` as needed

## Default workflow

1. Read the user's career profile and target constraints.
2. Run job discovery and collect real JD data.
3. Shortlist the most relevant roles.
4. Run fit analysis on shortlisted roles.
5. Pick the strongest targets.
6. Generate or update tailored resume versions.
7. Build interview preparation packs for top targets.
8. Return a ranked action plan.

## When to narrow scope

If the user asks for only one step, do that step instead of forcing the full pipeline.
Examples:

- only find jobs
- only analyze a JD
- only tailor a resume
- only prepare interview questions

## Hard rules

- Do not pretend the full pipeline ran if some parts failed.
- Preserve partial progress and report what completed.
- Do not rely on list-page titles when detail pages are required and available.
- Stop retrying brittle website actions after 3 failures on the same item.
- Keep the user's background truthful across all downstream steps.

## Recommended decision flow

### Job discovery stage

Keep only roles that are plausibly relevant to the user's target path.

### Fit stage

Separate:
- strong targets
- stretch targets
- low-value targets

### Resume stage

Tailor only for strong targets or explicitly requested stretch targets.

### Interview stage

Build deeper prep only for roles that survive the fit stage.

## Output contract

Return these sections:

1. pipeline status
2. target summary
3. shortlisted roles
4. fit-analysis highlights
5. tailored-resume plan or generated versions
6. interview-prep plan or generated packs
7. blocked items / failures
8. recommended next actions

## Notes

This skill is the orchestrator.
It should call other skills conceptually and keep each component focused on its own job.
