#!/usr/bin/env python3
"""Minimal Crawl4AI-backed JD extraction scaffold.

Current state:
- Defines stable CLI and structured JSON contract for JD extraction.
- Detects whether crawl4ai is installed.
- Keeps validation and downstream schema explicit.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from importlib.util import find_spec
from typing import Any, Dict, List


@dataclass
class JDRecord:
    title: str
    company: str
    city: str
    salary: str
    responsibilities: List[str]
    requirements: List[str]
    preferred_skills: List[str]
    education_requirement: str
    experience_requirement: str
    source_url: str
    extraction_confidence: str


@dataclass
class JDExtractResult:
    ok: bool
    source: str
    source_url: str
    timestamp_utc: str
    record: Dict[str, Any]
    failures: List[Dict[str, str]]
    note: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def crawl4ai_available() -> bool:
    return find_spec("crawl4ai") is not None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Extract JD detail with Crawl4AI scaffold")
    p.add_argument("--source", required=True, help="source name, e.g. 51job | liepin | shixiseng")
    p.add_argument("--url", required=True, help="detail page URL")
    p.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    return p


def empty_record(url: str) -> Dict[str, Any]:
    return asdict(
        JDRecord(
            title="",
            company="",
            city="",
            salary="",
            responsibilities=[],
            requirements=[],
            preferred_skills=[],
            education_requirement="",
            experience_requirement="",
            source_url=url,
            extraction_confidence="none",
        )
    )


def missing_dependency_result(source: str, url: str) -> JDExtractResult:
    return JDExtractResult(
        ok=False,
        source=source,
        source_url=url,
        timestamp_utc=utc_now(),
        record=empty_record(url),
        failures=[
            {
                "type": "dependency-missing",
                "message": "crawl4ai is not installed in the current environment",
            }
        ],
        note="Scaffold is ready, but live JD extraction requires crawl4ai plus a source-specific extraction handler.",
    )


def not_implemented_result(source: str, url: str) -> JDExtractResult:
    return JDExtractResult(
        ok=False,
        source=source,
        source_url=url,
        timestamp_utc=utc_now(),
        record=empty_record(url),
        failures=[
            {
                "type": "source-not-implemented",
                "message": f"JD extraction handler for '{source}' has not been implemented yet",
            }
        ],
        note="Implement a source-specific detail-page extraction function and validate body sections before claiming success.",
    )


def main() -> int:
    args = build_parser().parse_args()

    if not crawl4ai_available():
        result = missing_dependency_result(args.source, args.url)
    else:
        # Future extension point:
        # if args.source == "51job":
        #     result = extract_51job_jd(args.url)
        # elif args.source == "liepin":
        #     result = extract_liepin_jd(args.url)
        # else:
        result = not_implemented_result(args.source, args.url)

    payload = asdict(result)
    if args.pretty:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
