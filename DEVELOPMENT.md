# Family Filter — maintenance

> Internal maintainer notes. Product overview: [README](README.md).

Family-shared AdGuard custom filter distribution. The published list combines
the family's explicit allowlist, narrowly scoped compatibility exceptions, and
reviewed site-specific ad or decluttering rules.

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
