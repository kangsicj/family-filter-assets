#!/usr/bin/env python3
"""Build and validate the published AdGuard filter from reviewed sources."""

from __future__ import annotations

import argparse
import difflib
import ipaddress
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "filter-src"
ALLOWLIST_PATH = SOURCE_DIR / "allowlist.txt"
METADATA_PATH = SOURCE_DIR / "metadata.json"
RULES_PATH = SOURCE_DIR / "rules.txt"
OUTPUT_PATH = ROOT / "docs" / "filters" / "2026" / "7f3a91c2-family.txt"

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?$"
)
GLOBAL_COSMETIC_PREFIXES = ("##", "#@#", "#$#", "#?#", "#%#", "#$?#")


class FilterSourceError(ValueError):
    """Raised when a source file violates the repository policy."""


def load_metadata() -> dict[str, str]:
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    required = {
        "title",
        "description",
        "homepage",
        "source",
        "version",
        "last_modified",
        "expires",
    }
    missing = sorted(required - metadata.keys())
    if missing:
        raise FilterSourceError(f"metadata is missing: {', '.join(missing)}")
    return metadata


def is_valid_host(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return bool(DOMAIN_RE.fullmatch(host))


def load_allowlist() -> list[str]:
    hosts: list[str] = []
    for line_number, raw_line in enumerate(
        ALLOWLIST_PATH.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        host = line.lower().rstrip(".")
        if "://" in host or "/" in host or "^" in host or "$" in host:
            raise FilterSourceError(
                f"{ALLOWLIST_PATH}:{line_number}: expected a host, got {line!r}"
            )
        if not is_valid_host(host):
            raise FilterSourceError(
                f"{ALLOWLIST_PATH}:{line_number}: invalid host {line!r}"
            )
        hosts.append(host)

    duplicates = sorted({host for host in hosts if hosts.count(host) > 1})
    if duplicates:
        raise FilterSourceError(f"duplicate allowlist hosts: {', '.join(duplicates)}")
    return hosts


def collapse_covered_hosts(hosts: list[str]) -> tuple[list[str], dict[str, str]]:
    """Remove subdomains already covered by an explicit parent-domain rule."""
    host_set = set(hosts)
    effective: list[str] = []
    covered_by: dict[str, str] = {}

    for host in sorted(hosts):
        try:
            ipaddress.ip_address(host)
        except ValueError:
            labels = host.split(".")
            parent = next(
                (
                    candidate
                    for index in range(1, len(labels) - 1)
                    if (candidate := ".".join(labels[index:])) in host_set
                ),
                None,
            )
            if parent is not None:
                covered_by[host] = parent
                continue
        effective.append(host)

    return effective, covered_by


def load_site_rules() -> list[str]:
    lines = [line.rstrip() for line in RULES_PATH.read_text(encoding="utf-8").splitlines()]
    rules = [line for line in lines if line and not line.startswith("!")]

    duplicates = sorted({rule for rule in rules if rules.count(rule) > 1})
    if duplicates:
        raise FilterSourceError(f"duplicate site rules: {', '.join(duplicates)}")

    for line_number, line in enumerate(lines, start=1):
        if not line or line.startswith("!"):
            continue
        if line.startswith(GLOBAL_COSMETIC_PREFIXES) or line.startswith("*#"):
            raise FilterSourceError(
                f"{RULES_PATH}:{line_number}: global cosmetic rules are forbidden; "
                "scope the rule to one or more reviewed domains"
            )
    return lines


def render_filter() -> tuple[str, int, int, int]:
    metadata = load_metadata()
    source_hosts = load_allowlist()
    effective_hosts, covered_by = collapse_covered_hosts(source_hosts)
    site_lines = load_site_rules()

    header = [
        f"! Title: {metadata['title']}",
        f"! Description: {metadata['description']}",
        f"! Homepage: {metadata['homepage']}",
        f"! Source: {metadata['source']}",
        f"! Version: {metadata['version']}",
        f"! Last modified: {metadata['last_modified']}",
        f"! Expires: {metadata['expires']}",
        "! Syntax: AdGuard",
        "!",
        "! Full-document allowlist imported from the family's AdGuard extension.",
        "! These rules intentionally disable filtering on the matched host and subdomains.",
        (
            f"! Source hosts: {len(source_hosts)}; effective rules: {len(effective_hosts)}; "
            f"covered subdomains collapsed: {len(covered_by)}."
        ),
        "!",
    ]
    allowlist_rules = [f"@@||{host}^$document" for host in effective_hosts]
    content = "\n".join(header + allowlist_rules + ["", *site_lines]).rstrip() + "\n"
    site_rule_count = sum(1 for line in site_lines if line and not line.startswith("!"))
    return content, len(source_hosts), len(effective_hosts), site_rule_count


def check_or_write(check: bool) -> int:
    expected, source_count, effective_count, site_rule_count = render_filter()
    existing = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""

    if check:
        if existing != expected:
            diff = difflib.unified_diff(
                existing.splitlines(keepends=True),
                expected.splitlines(keepends=True),
                fromfile=str(OUTPUT_PATH),
                tofile="generated filter",
            )
            sys.stderr.writelines(diff)
            print("Published filter is stale. Run: python scripts/build_filter.py", file=sys.stderr)
            return 1
        action = "validated"
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(expected, encoding="utf-8", newline="\n")
        action = "built"

    print(
        f"{action} {OUTPUT_PATH.relative_to(ROOT)}: "
        f"{source_count} source hosts -> {effective_count} allowlist rules; "
        f"{site_rule_count} site rules"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate sources and fail if the published filter is not up to date",
    )
    args = parser.parse_args()
    try:
        return check_or_write(args.check)
    except (FilterSourceError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
