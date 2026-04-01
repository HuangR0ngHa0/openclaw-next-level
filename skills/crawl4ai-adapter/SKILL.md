---
name: crawl4ai-adapter
description: Use Crawl4AI as the primary crawling and structured-extraction layer for dynamic websites, search-result pages, detail pages, and discussion posts. Activate when browser-only clicking is brittle, when websites rerender or anti-bot behavior makes homepage interaction unstable, or when the task needs structured extraction from job boards, company pages, interview writeups, social posts, or other dynamic web pages.
---

# Crawl4AI Adapter

Use Crawl4AI as the extraction engine. Keep business decisions in higher-level skills.

## When to use

Use this adapter when:

- homepage search boxes are unstable
- browser refs rerender too often
- dynamic content needs scrolling / waiting / extraction
- detail pages must be parsed into structured output
- LLM-friendly markdown or JSON extraction is needed
- the workflow depends on real content, not just visible snippets

Typical career-automation cases:

- job search result pages
- job detail pages / JD pages
- company pages
- interview experience posts
- discussion threads related to companies or roles

## Core principle

Do not let higher-level skills reinvent crawling.

- `job-intelligence` should call Crawl4AI for result pages and JD pages.
- `interview-prep-builder` should call Crawl4AI for interview writeups and discussion pages.
- Site-specific adapters should only describe entry rules, validation rules, and extraction schema.

## Preferred workflow

1. Prefer direct navigation to stable search-result URLs or known detail URLs.
2. Avoid homepage search-box interaction unless there is no better option.
3. Extract raw page content into markdown and/or structured records.
4. Validate that the extracted page is the intended page type.
5. Return structured output plus failure notes.

## Hard rules

- Prefer result-page URLs and detail-page URLs over homepage interaction.
- Do not claim a JD was captured unless responsibilities/requirements or equivalent body sections were extracted.
- Do not summarize from titles alone when the task requires detail-page content.
- If a site triggers anti-bot behavior repeatedly, stop and return a clear failure category.
- Preserve partial results instead of pretending success.

## Recommended output modes

Choose one or more based on task:

- markdown output for readable downstream summarization
- structured JSON for stable pipeline steps
- screenshots only for debugging, not as the primary business output

## Career-oriented schemas

### Job list item
- title
- company
- city
- salary
- experience_requirement
- education_requirement
- tags
- detail_url
- source

### JD detail
- title
- company
- city
- salary
- responsibilities
- requirements
- preferred_skills
- education_requirement
- experience_requirement
- source_url
- extraction_confidence

### Interview/discussion post
- title
- company
- role
- source_platform
- author_if_available
- date_if_available
- body_summary
- question_list
- notable_claims
- source_url
- extraction_confidence

## Failure taxonomy

Use categories like:

- anti-bot-suspected
- login-wall
- dynamic-rerender
- result-page-empty
- detail-page-empty
- wrong-page-type
- extraction-schema-miss
- timeout

## Notes for this workspace

This adapter is intended to replace brittle homepage click loops with a more robust crawl-first strategy.
Keep user-specific ranking, fit analysis, resume tailoring, and interview preparation in the higher-level career skills.
