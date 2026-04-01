# Crawl4AI Strategy for Career Automation

## Goal

Use Crawl4AI as the default extraction layer for dynamic career-related web sources, while keeping ranking, fit analysis, resume tailoring, and interview preparation in OpenClaw skills.

## Architectural split

### Crawl layer
Use Crawl4AI for:
- job search result pages
- job detail pages
- company info pages
- interview writeups
- discussion / social posts when page extraction is needed

### Business logic layer
Use OpenClaw skills for:
- job filtering and ranking
- JD fit analysis
- resume tailoring
- interview prep generation
- orchestration and memory

## Source priority

### Priority A: primary JD / job sources
- 前程无忧 search-result pages
- 猎聘 search-result pages
- 实习僧 search-result pages
- company career pages

### Priority B: interview / discussion sources
- 牛客
- 小红书
- public company discussion pages

### Priority C: degraded / fallback sources
- BOSS (only when stable; otherwise downgrade immediately)

## Retrieval rules

1. Prefer direct result-page or detail-page URLs.
2. Avoid homepage search-box interaction unless unavoidable.
3. Validate page type before trusting extraction.
4. Only pass high-confidence JD bodies into fit analysis.
5. Keep source-level failures explicit.

## Minimal viable pipeline

1. Pick one source and one query.
2. Crawl the search-result page.
3. Extract top relevant result cards.
4. Crawl 1-3 detail pages.
5. Validate and extract one full JD.
6. Feed the JD to:
   - `jd-fit-analyzer`
   - `resume-tailor`
   - `interview-prep-builder`
7. Optionally crawl 牛客 / 小红书 for interview context.

## Suggested first queries

- 机器人 C++ 广州
- ROS C++ 深圳
- 自动驾驶 C++ 广州
- 机器人软件 深圳
- SLAM 定位 广州
- 感知 定位 机器人 深圳

## Page validation heuristics

### Search-result page should contain
- multiple role cards
- at least title/company/city or equivalent
- detail links or navigable targets

### JD page should contain
- role title
- company name
- job body sections such as responsibilities / requirements / 任职要求 / 岗位职责

### Interview post page should contain
- body text beyond title
- role/company clues or explicit mention
- real question / experience content when possible

## Failure handling

Stop early and surface failure if:
- anti-bot behavior is repeatedly triggered
- result page is empty or unrelated
- extracted detail page is not actually a JD page
- page content is too thin for downstream decisions

## Next implementation steps

1. Add a minimal `scripts/crawl4ai/` scaffold.
2. Add source-specific schema references if needed.
3. Wire `job-intelligence` and `interview-prep-builder` to mention `crawl4ai-adapter` explicitly.
4. Run one real source end-to-end.
