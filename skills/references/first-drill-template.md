# First Drill Template

Use this file to run the first end-to-end career-pipeline exercise against a real job.

## Goal

Validate whether the current skill architecture can support a realistic flow:

1. collect a real JD
2. analyze fit
3. tailor the resume
4. build an interview prep pack
5. report blockers and next actions

## Recommended drill scope

For the first run, use **one real role only**.
Do not try to batch many jobs yet.

Prefer a role that is:

- in Guangzhou or Shenzhen
- robotics / autonomous driving / C++ / ROS / Linux related
- not obviously fake or low-quality
- reachable from a current BOSS detail page if possible

## Inputs to prepare

### Required
- target company name
- target role title
- target city
- source JD URL or browser page
- full JD text if page extraction succeeds

### References to read
- `skills/references/user-career-profile.md`
- `skills/references/resume-master.md`
- `skills/job-intelligence/SKILL.md`
- `skills/jd-fit-analyzer/SKILL.md`
- `skills/resume-tailor/SKILL.md`
- `skills/interview-prep-builder/SKILL.md`

### Optional supporting sources
- `skills/boss-adapter/SKILL.md`
- `skills/xiaohongshu-adapter/SKILL.md`

## Drill procedure

### Stage 1: JD collection

Objective:
- open the real job detail page
- extract actual JD content
- avoid relying on list titles alone

Success criteria:
- company, title, city, and most of the JD body are captured

Fail conditions:
- detail page cannot be opened after 3 attempts
- JD body is empty or clearly incomplete

If failed:
- record the failure type
- stop forcing the page
- either switch to another real role or ask for a manually supplied JD

### Stage 2: Fit analysis

Objective:
- compare the JD against the user's real profile

Expected output:
- strong matches
- partial matches
- clear gaps
- whether the role is worth applying to

### Stage 3: Resume tailoring

Objective:
- generate a role-specific resume adjustment plan or a full tailored draft

Expected output:
- tailored summary
- revised bullet points
- skill ordering changes
- unresolved gaps

### Stage 4: Interview prep

Objective:
- generate a realistic prep pack tied to the JD and the user's real projects

Expected output:
- technical focus areas
- likely deep-dive questions
- HR questions
- answer angles
- questions to ask interviewer

### Stage 5: Final report

Return these sections:

1. role snapshot
2. jd extraction quality
3. fit verdict
4. resume-tailoring summary
5. interview-prep summary
6. blockers and confidence notes
7. next recommended actions

## Practical notes

- Keep the first drill narrow and concrete.
- Prefer honesty and partial completion over pretending the whole flow worked.
- If BOSS is unstable, fall back to using a manually provided JD for the downstream stages.
- The point of the first drill is to expose weak points in the workflow, not to look perfect.
