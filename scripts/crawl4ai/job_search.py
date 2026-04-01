#!/usr/bin/env python3
"""Minimal Crawl4AI-backed job search scaffold.

Current state:
- Defines stable CLI and JSON output schema.
- Detects whether crawl4ai is installed.
- Does NOT pretend live crawling already works when the dependency is absent.
- Designed to be expanded source-by-source.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from importlib.util import find_spec
from typing import Any, Dict, List, Optional


@dataclass
class JobCard:
    title: str
    company: str
    city: str
    salary: str
    experience_requirement: str
    education_requirement: str
    tags: List[str]
    detail_url: str
    source: str
    extraction_confidence: str


@dataclass
class JobSearchResult:
    ok: bool
    source: str
    query: str
    city: str
    timestamp_utc: str
    cards: List[Dict[str, Any]]
    failures: List[Dict[str, str]]
    note: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def crawl4ai_available() -> bool:
    return find_spec("crawl4ai") is not None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Search job pages with Crawl4AI scaffold")
    p.add_argument("--source", required=True, help="job source, e.g. 51job | liepin | shixiseng")
    p.add_argument("--query", required=True, help="search query, e.g. 机器人 C++")
    p.add_argument("--city", default="", help="target city, e.g. 广州")
    p.add_argument("--limit", type=int, default=10, help="max cards to return")
    p.add_argument("--url", default="", help="optional direct result-page URL")
    p.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    return p


def not_ready_result(source: str, query: str, city: str) -> JobSearchResult:
    return JobSearchResult(
        ok=False,
        source=source,
        query=query,
        city=city,
        timestamp_utc=utc_now(),
        cards=[],
        failures=[
            {
                "type": "dependency-missing",
                "message": "crawl4ai is not installed in the current environment",
            }
        ],
        note="Scaffold is in place, but live crawling is not enabled until crawl4ai is installed and source handlers are implemented.",
    )


def source_not_implemented_result(source: str, query: str, city: str) -> JobSearchResult:
    return JobSearchResult(
        ok=False,
        source=source,
        query=query,
        city=city,
        timestamp_utc=utc_now(),
        cards=[],
        failures=[
            {
                "type": "source-not-implemented",
                "message": f"source handler for '{source}' has not been implemented yet",
            }
        ],
        note="Implement a source-specific crawl function that targets stable result-page URLs and emits normalized job cards.",
    )


def main() -> int:
    args = build_parser().parse_args()

    if not crawl4ai_available():
        result = not_ready_result(args.source, args.query, args.city)
    else:
        # Future extension point:
        # if args.source == "51job":
        #     result = crawl_51job(...)
        # elif args.source == "liepin":
        #     result = crawl_liepin(...)
        # else:
        result = source_not_implemented_result(args.source, args.query, args.city)

    payload = asdict(result)
    if args.pretty:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
