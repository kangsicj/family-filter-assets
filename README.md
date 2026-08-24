# Family Filter Assets

Family-shared AdGuard custom filter distribution. The published list combines
the family's explicit allowlist, narrowly scoped compatibility exceptions, and
reviewed site-specific ad or decluttering rules.

## AdGuard subscription URL

Add this URL as a custom filter in AdGuard:

```text
https://kangsicj.github.io/family-filter-assets/filters/2026/7f3a91c2-family.txt
```

## Allowlist behavior

`filter-src/allowlist.txt` contains all 192 hosts imported from the AdGuard
browser extension. The build emits 171 effective `@@||host^$document` rules;
21 child hosts are omitted because an explicitly listed parent already covers
them.

`$document` is a full filtering exception. It disables network, cosmetic, HTML,
and script-based filtering on the matched host and its subdomains, including
rules from other enabled filter lists. Keep an entry only when that broad
exception is intentional.

## Korean site coverage

This list keeps custom rules site-scoped to reduce false positives. It includes
family-specific coverage for Naver, Daum, Nate, Zum, several Korean communities,
and selected streaming sites. The Nate and Zum selectors and the updated Naver
and Daum selectors were checked against live pages on 2026-07-14.

For broad Korean advertising coverage, enable
[List-KR](https://github.com/List-KR/List-KR) in AdGuard as the maintained base
list. This repository is an additive family override, not a replacement for a
full regional filter.

## Maintenance

Source files:

- `filter-src/allowlist.txt`: auditable raw host allowlist
- `filter-src/rules.txt`: reviewed compatibility, blocking, and decluttering rules
- `filter-src/metadata.json`: published filter metadata

The published filter is kept synchronized with the reviewed source rules before
CI validation and distribution. Any rule change must update the generated filter
from the source with `python scripts/build_filter.py` before pushing.

Rebuild and verify the published file:

```text
python scripts/build_filter.py
python scripts/build_filter.py --check
npx --yes @adguard/aglint@3.0.2 docs/filters/2026/7f3a91c2-family.txt filter-src/rules.txt
```

The generator rejects duplicate hosts, invalid hosts, duplicate site rules, and
unscoped global cosmetic rules. CI also parses both rule files with AdGuard's
AGLint.

## GitHub Pages setup

Repository settings:

```text
Settings -> Pages -> Deploy from a branch
Branch: main
Folder: /docs
```

Only the generated filter under `docs/filters/2026/7f3a91c2-family.txt` is
intended to be subscribed to directly.
