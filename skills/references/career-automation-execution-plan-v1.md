# Career Automation Execution Plan v1

## Status

Active default pipeline as of 2026-04-02:

- Primary extraction layer: `skills/miliger-playwright-scraper`
- Secondary browser fallback / debugging layer: `skills/playwright`
- Business orchestration layer: `skills/career-pipeline`
- Supporting business skills:
  - `skills/job-intelligence`
  - `skills/jd-fit-analyzer`
  - `skills/resume-tailor`
  - `skills/interview-prep-builder`

## Explicit decision

The previous homepage-driven web-search approach is abandoned.
Do NOT default to:
- typing into unstable homepage search boxes
- brittle multi-click search chains
- direct dependence on Crawl4AI for logged-in or anti-bot-heavy result pages

Crawl4AI remains available only as an optional degraded fallback for public/stable detail URLs.

## Goal

Build a reliable end-to-end chain for the user's job search:
1. open a stable result page in a real browser
2. extract candidate job cards
3. open detail pages and extract real JD text
4. normalize output into structured records
5. pass shortlisted roles into fit analysis, resume tailoring, and interview prep

## Preferred execution order

### Stage 1 — result-page extraction
Use `miliger-playwright-scraper` as the first choice when:
- the page is JS-rendered
- result cards appear only after dynamic loading
- scrolling / tab switching / click expansion is needed

Output target:
- source
- query
- city
- result page URL
- extracted cards[] with:
  - title
  - company
  - city
  - salary
  - experience requirement
  - education requirement
  - tags
  - detail URL
  - extraction confidence

### Stage 2 — detail-page extraction
For each shortlisted card:
- prefer opening the real detail page in browser flow
- extract visible JD text and key metadata
- save raw markdown/text snapshot before downstream interpretation

Output target:
- title
- company
- city
- salary
- responsibilities[]
- requirements[]
- preferred_skills[]
- education_requirement
- experience_requirement
- source_url
- extraction_confidence

### Stage 3 — business filtering
Use `job-intelligence` rules to:
- keep Guangzhou / Shenzhen robotics / autonomous driving / C++ / ROS / Linux relevant roles
- reject training / outsourcing traps / fake technical roles
- separate apply / maybe / skip

### Stage 4 — downstream value generation
For strong targets only:
- run JD fit analysis
- tailor resume emphasis
- build interview prep packs

## Site strategy

### Priority sources
1. 51job public result/detail pages when accessible via stable browser flow
2. Liepin stable result/detail pages when accessible
3. Shixiseng for intern / campus roles
4. Company career pages when available

### Degraded / optional sources
- BOSS: optional fallback only
- 牛客: interview-prep signal, not primary JD source
- 小红书: company / interview discussion supplement, not primary JD source

## Hard rules

- Do not claim end-to-end automation succeeded unless the actual result page and detail page were both extracted.
- Do not rely on list-page snippets when detail pages are reachable.
- Stop repeating the same fragile action after 3 failures.
- Report blocked items explicitly.
- Keep the user's background truthful in all downstream outputs.

## Current repo implication

Existing files under `scripts/crawl4ai/` are no longer the default front door.
They should be treated as fallback extraction scaffolds, not the primary workflow.

## Next implementation target

Create a Playwright-first extraction path that can produce:
- `artifacts/jobs/<source>/<date>/cards.json`
- `artifacts/jobs/<source>/<date>/details/<job-id>.json`
- `artifacts/jobs/<source>/<date>/details/<job-id>.md`
- `artifacts/jobs/<source>/<date>/summary.md`

The first successful validation should focus on one source and one search result page, not all sources at once.
