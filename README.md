<div align="center">

<img src=".github/assets/banner.svg" alt="Family Filter — a calm, ad-free web for the whole family" width="100%">

<br>

[![Validate filter](https://github.com/kangsicj/family-filter-assets/actions/workflows/validate-filter.yml/badge.svg)](https://github.com/kangsicj/family-filter-assets/actions/workflows/validate-filter.yml)
<a href="https://kangsicj.github.io/family-filter-assets/filters/2026/7f3a91c2-family.txt"><img src="https://img.shields.io/badge/AdGuard-custom%20filter-68BC71?style=for-the-badge&logo=adguard&logoColor=white" alt="AdGuard custom filter"></a>
<a href="https://kangsicj.github.io/family-filter-assets/filters/2026/7f3a91c2-family.txt"><img src="https://img.shields.io/badge/GitHub-Pages-222222?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Pages"></a>
<a href="https://fairy.hada.io/@jinny"><img src="https://img.shields.io/badge/Fairy-Sponsor-FF6FB5?style=for-the-badge&logo=githubsponsors&logoColor=white" alt="Fairy Sponsor"></a>

**The family's shared AdGuard filter: an auditable allowlist, narrowly scoped compatibility<br>exceptions and reviewed site-specific ad & clutter rules.**

[Subscribe](#-subscribe) · [What it does](#-what-it-does) · [Docs](#-documentation) · [Support](#-support)

</div>

---

## 🔔 Subscribe

<div align="center">

[**➕ Add to AdGuard**](https://subscribe.adblockplus.org/?location=https%3A%2F%2Fkangsicj.github.io%2Ffamily-filter-assets%2Ffilters%2F2026%2F7f3a91c2-family.txt&title=Family%20Filter)

</div>

Or add this URL as a custom filter in AdGuard:

```text
https://kangsicj.github.io/family-filter-assets/filters/2026/7f3a91c2-family.txt
```

## ✨ What it does

<table>
<tr>
<td width="33%" valign="top">

### ✅ Allowlist
Hosts the family relies on, kept auditable in plain text.

</td>
<td width="33%" valign="top">

### 🇰🇷 Korean sites
Site-scoped cleanup for Naver, Daum, Nate, Zum, communities and streaming.

</td>
<td width="33%" valign="top">

### 🧪 CI-validated
Every change is parsed by AGLint and rebuilt reproducibly.

</td>
</tr>
</table>

## 📚 Documentation

### Allowlist behavior

`filter-src/allowlist.txt` contains all 192 hosts imported from the AdGuard
browser extension. The build emits 171 effective `@@||host^$document` rules;
21 child hosts are omitted because an explicitly listed parent already covers
them.

`$document` is a full filtering exception. It disables network, cosmetic, HTML,
and script-based filtering on the matched host and its subdomains, including
rules from other enabled filter lists. Keep an entry only when that broad
exception is intentional.

### Korean site coverage

This list keeps custom rules site-scoped to reduce false positives. It includes
family-specific coverage for Naver, Daum, Nate, Zum, several Korean communities,
and selected streaming sites. The Nate and Zum selectors and the updated Naver
and Daum selectors were checked against live pages on 2026-07-14.

For broad Korean advertising coverage, enable
[List-KR](https://github.com/List-KR/List-KR) in AdGuard as the maintained base
list. This repository is an additive family override, not a replacement for a
full regional filter.

### Maintenance

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

### GitHub Pages setup

Repository settings:

```text
Settings -> Pages -> Deploy from a branch
Branch: main
Folder: /docs
```

Only the generated filter under `docs/filters/2026/7f3a91c2-family.txt` is
intended to be subscribed to directly.

## 💖 Support

This is a personal project built in spare time. If it helps you, you can support its development on **Fairy** — it goes to hosting costs and development time.

<a href="https://fairy.hada.io/@jinny"><img src="https://img.shields.io/badge/%F0%9F%A7%9A%20Support%20on%20Fairy-FF6FB5?style=for-the-badge" alt="Support on Fairy"></a>

<div align="right"><sub>Made with ♥ by <a href="https://github.com/kangsicj">@kangsicj</a></sub></div>
