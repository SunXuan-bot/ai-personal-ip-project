#!/usr/bin/env python3
"""Fetch lightweight WeChat article leads from Sogou Weixin search.

This script only collects public search-result snippets as leads. It does not
log in, bypass platform restrictions, or crawl full WeChat account histories.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "03_选题库" / "公众号线索"


def fetch(query: str) -> str:
    url = "https://weixin.sogou.com/weixin?" + urllib.parse.urlencode(
        {"type": "2", "query": query}
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def clean(fragment: str) -> str:
    return html.unescape(re.sub(r"<.*?>", "", fragment or "").strip())


def clean_date(fragment: str) -> str:
    value = clean(fragment)
    match = re.search(r"timeConvert\('(\d+)'\)", value)
    if match:
        timestamp = int(match.group(1))
        return dt.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    return value


def parse_results(page: str, query: str) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    blocks = re.findall(
        r'<div class="txt-box">(.*?)(?=<div class="txt-box">|</ul>)',
        page,
        flags=re.S,
    )
    for block in blocks:
        title_match = re.search(r"<h3>.*?</h3>", block, flags=re.S)
        href_match = re.search(r'href="([^"]+)"', block)
        source_match = re.search(r'class="account"[^>]*>(.*?)</a>', block, flags=re.S)
        date_match = re.search(r'class="s2"[^>]*>(.*?)</span>', block, flags=re.S)
        summary_match = re.search(r'<p class="txt-info">(.*?)</p>', block, flags=re.S)

        href = html.unescape(href_match.group(1)) if href_match else ""
        if href.startswith("/"):
            href = "https://weixin.sogou.com" + href

        title = clean(title_match.group(0) if title_match else "")
        if not title:
            continue

        results.append(
            {
                "query": query,
                "title": title,
                "source": clean(source_match.group(1) if source_match else ""),
                "date": clean_date(date_match.group(1) if date_match else ""),
                "summary": clean(summary_match.group(1) if summary_match else ""),
                "sogou_url": href,
                "status": "sogou_lead_only",
            }
        )
    return results


def write_outputs(results: list[dict[str, str]]) -> tuple[Path, Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    json_path = OUT_DIR / f"{stamp}_武汉AI公众号线索.json"
    md_path = OUT_DIR / f"{stamp}_武汉AI公众号线索.md"

    json_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# 武汉 AI 公众号线索",
        "",
        f"生成时间：{stamp}",
        "",
        "说明：以下只是不带登录态的搜狗微信搜索线索，正式口播前需补原文或官网核验。",
        "",
        "| 关键词 | 标题 | 来源 | 日期 | 状态 | 链接 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in results:
        lines.append(
            "| {query} | {title} | {source} | {date} | {status} | {url} |".format(
                query=item["query"].replace("|", " "),
                title=item["title"].replace("|", " "),
                source=item["source"].replace("|", " "),
                date=item["date"].replace("|", " "),
                status=item["status"],
                url=item["sogou_url"],
            )
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("queries", nargs="+", help="Sogou Weixin search keywords")
    args = parser.parse_args()

    all_results: list[dict[str, str]] = []
    for query in args.queries:
        page = fetch(query)
        all_results.extend(parse_results(page, query))

    json_path, md_path = write_outputs(all_results)
    print(f"results={len(all_results)}")
    print(f"json={json_path}")
    print(f"markdown={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
