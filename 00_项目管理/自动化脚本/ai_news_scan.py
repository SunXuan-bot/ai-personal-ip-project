#!/usr/bin/env python3
"""Fetch AI HOT selected items and write a local review draft."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None


PROJECT_ROOT = Path(
    os.environ.get("AI_NEWS_SCAN_PROJECT_ROOT", Path(__file__).resolve().parents[2])
)
OUTPUT_DIR = Path(
    os.environ.get(
        "AI_NEWS_SCAN_OUTPUT_DIR",
        PROJECT_ROOT / "04_脚本与内容" / "AI资讯日更" / "自动筛选",
    )
)
LOG_DIR = Path(
    os.environ.get(
        "AI_NEWS_SCAN_LOG_DIR",
        PROJECT_ROOT / "00_项目管理" / "自动化日志",
    )
)
BASE_URL = "https://aihot.virxact.com/api/public/items"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 "
    "Safari/537.36 aihot-skill/0.2.0 ai-personal-ip-scheduler/0.1.0"
)


def local_tz():
    if ZoneInfo:
        return ZoneInfo("Asia/Shanghai")
    return timezone(timedelta(hours=8))


def now_local() -> datetime:
    return datetime.now(local_tz())


def utc_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_items(hours: int = 24, take: int = 80) -> list[dict]:
    since = utc_iso(datetime.now(timezone.utc) - timedelta(hours=hours))
    params = urllib.parse.urlencode(
        {"mode": "selected", "since": since, "take": str(take)}
    )
    req = urllib.request.Request(
        f"{BASE_URL}?{params}",
        headers={"User-Agent": UA, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("items", [])


AI_BIG_WORDS = [
    "openai",
    "anthropic",
    "google",
    "gemini",
    "deepmind",
    "meta",
    "llama",
    "microsoft",
    "azure",
    "xai",
    "grok",
    "deepseek",
    "qwen",
    "通义",
    "阿里",
    "字节",
    "豆包",
    "seed",
    "minimax",
    "moonshot",
    "kimi",
    "智谱",
    "glm",
    "阶跃",
    "baichuan",
    "模型",
    "大模型",
    "多模态",
    "语音",
    "视频",
    "图像",
    "智能体",
    "agent",
    "coding",
    "编程",
    "api",
    "开源",
    "发布",
    "上线",
    "更新",
    "benchmark",
]

PRACTICAL_WORDS = [
    "工具",
    "产品",
    "工作流",
    "插件",
    "浏览器",
    "剪辑",
    "写作",
    "办公",
    "开发者",
    "创作者",
    "企业",
    "应用",
    "demo",
    "演示",
]

VISUAL_WORDS = [
    "youtube",
    "视频",
    "demo",
    "演示",
    "发布会",
    "voice",
    "语音",
    "image",
    "图像",
    "video",
    "机器人",
    "眼镜",
    "产品",
]

LOW_VALUE_WORDS = [
    "融资",
    "估值",
    "股价",
    "上市",
    "财报",
    "裁员",
]


def text_of(item: dict) -> str:
    fields = [
        item.get("title"),
        item.get("titleZh"),
        item.get("summary"),
        item.get("summaryZh"),
        item.get("sourceName"),
        item.get("source"),
        item.get("category"),
    ]
    return " ".join(str(x) for x in fields if x).lower()


def item_title(item: dict) -> str:
    return (
        item.get("titleZh")
        or item.get("title")
        or item.get("name")
        or "未命名条目"
    )


def item_summary(item: dict) -> str:
    return item.get("summaryZh") or item.get("summary") or ""


def source_url(item: dict) -> str:
    return item.get("sourceUrl") or item.get("url") or item.get("link") or ""


def source_name(item: dict) -> str:
    return item.get("sourceName") or item.get("source") or "未知来源"


def published_at(item: dict) -> str:
    return item.get("publishedAt") or item.get("createdAt") or ""


def score_item(item: dict) -> tuple[int, list[str], list[str]]:
    txt = text_of(item)
    score = 0
    reasons: list[str] = []
    cautions: list[str] = []

    big_hits = [w for w in AI_BIG_WORDS if w in txt]
    practical_hits = [w for w in PRACTICAL_WORDS if w in txt]
    visual_hits = [w for w in VISUAL_WORDS if w in txt]
    low_hits = [w for w in LOW_VALUE_WORDS if w in txt]

    category = str(item.get("category") or "").lower()
    if category in {"ai-models", "ai-products"}:
        score += 4
        reasons.append("模型/产品更新，天然适合 AI 资讯主轴")
    elif category in {"industry", "tip"}:
        score += 2
        reasons.append("行业/观点类，可作为补充快讯")
    elif category == "paper":
        score += 1
        cautions.append("论文类需要确认能否快速讲清")

    if big_hits:
        score += min(5, len(set(big_hits)))
        reasons.append("命中 AI 圈高关注关键词：" + "、".join(sorted(set(big_hits))[:5]))

    if practical_hits:
        score += min(3, len(set(practical_hits)))
        reasons.append("可能和工具、创作者或小团队工作流相关")

    if visual_hits:
        score += 2
        reasons.append("可能有强关联画面素材或 Demo")

    if low_hits and not big_hits:
        score -= 3
        cautions.append("偏融资/股价/商业信息，和普通 AI 用户关系可能弱")
    elif low_hits:
        cautions.append("含商业/资本信息，需确认是否和 AI 圈判断强相关")

    summary = item_summary(item)
    if len(summary) >= 80:
        score += 1
        reasons.append("摘要信息量较足，便于压缩成口播")
    else:
        cautions.append("摘要偏短，需回源核验后再写")

    if source_url(item):
        score += 1
    else:
        cautions.append("缺少来源链接，发布前必须补来源")

    return score, reasons, cautions


def classify_rank(rank: int) -> str:
    labels = {
        1: "主新闻候选",
        2: "重点快讯",
        3: "重点快讯",
        4: "补充快讯",
        5: "补充快讯",
        6: "备选快讯",
    }
    return labels.get(rank, "候选")


def clean_md(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text.replace("|", "\\|")


def write_markdown(items: list[dict], run_time: datetime) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    slot = "1000" if run_time.hour < 13 else "1700"
    out_path = OUTPUT_DIR / f"{run_time:%Y-%m-%d}_{slot}_AI新闻候选筛选.md"

    scored = []
    for item in items:
        score, reasons, cautions = score_item(item)
        scored.append((score, item, reasons, cautions))
    scored.sort(key=lambda x: x[0], reverse=True)

    top = scored[:6]
    backup = scored[6:16]

    lines: list[str] = []
    lines.append(f"# {run_time:%Y-%m-%d %H:%M} AI 新闻候选筛选")
    lines.append("")
    lines.append("自动任务：每天 10:00、17:00 生成。")
    lines.append("")
    lines.append("## 筛选原则")
    lines.append("")
    lines.append("- 精准：优先 AI 圈当天会关注的大事。")
    lines.append("- 快速：优先能尽快核验、整理、录制和配素材的新闻。")
    lines.append("- 讲清楚：语言上能 10-20 秒说明事实和意义；画面上最好有官方视频、Demo、官网截图或数据卡。")
    lines.append("- 默认 5-6 条，质量不足时少讲，不为了凑数硬塞。")
    lines.append("")
    lines.append("## 建议入选 5-6 条")
    lines.append("")

    if not top:
        lines.append("本次没有拉到 AI HOT 精选条目，请检查网络或稍后重试。")
    for idx, (score, item, reasons, cautions) in enumerate(top, start=1):
        title = clean_md(item_title(item))
        summary = clean_md(item_summary(item))
        url = source_url(item)
        source = clean_md(source_name(item))
        pub = clean_md(published_at(item))
        lines.append(f"### {idx}. {title}")
        lines.append("")
        lines.append(f"- 定位：{classify_rank(idx)}")
        lines.append(f"- 初筛分：{score}")
        lines.append(f"- 来源：{source}")
        lines.append(f"- 发布时间：{pub or '待确认'}")
        lines.append(f"- 链接：{url or '待补'}")
        lines.append(f"- 摘要：{summary or '待回源补摘要'}")
        lines.append(f"- 选择理由：{'；'.join(reasons) if reasons else '待人工判断'}")
        lines.append(f"- 风险/边界：{'；'.join(cautions) if cautions else '暂无明显风险，但发布前仍需回源核验'}")
        lines.append("- 画面素材建议：优先找官方视频 / Demo；没有则找官网或产品页截图。")
        lines.append("- 用户反馈：")
        lines.append("")

    lines.append("## 备选池")
    lines.append("")
    for idx, (score, item, reasons, cautions) in enumerate(backup, start=1):
        title = clean_md(item_title(item))
        url = source_url(item)
        source = clean_md(source_name(item))
        reason = "；".join(reasons[:2]) if reasons else "待人工判断"
        lines.append(f"{idx}. {title}｜{source}｜分数 {score}｜{reason}｜{url}")

    lines.append("")
    lines.append("## 训练反馈区")
    lines.append("")
    lines.append("请你直接在这里标注，或复制给 Codex：")
    lines.append("")
    lines.append("```text")
    lines.append("像的新闻：")
    lines.append("不像的新闻：")
    lines.append("不够大的新闻：")
    lines.append("不好讲的新闻：")
    lines.append("可以做主新闻的：")
    lines.append("只能做快讯的：")
    lines.append("今天漏掉的重要新闻：")
    lines.append("```")
    lines.append("")
    lines.append("## 下一步")
    lines.append("")
    lines.append("- 你反馈后，我把标准写回优化记录。")
    lines.append("- 如确认主新闻，我再找强关联官方视频素材并写素材台账。")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    run_time = now_local()
    log_path = LOG_DIR / "ai_news_scan.log"
    try:
        items = fetch_items()
        out_path = write_markdown(items, run_time)
        msg = f"{run_time.isoformat()} OK wrote {out_path} items={len(items)}\n"
        log_path.open("a", encoding="utf-8").write(msg)
        print(msg, end="")
        return 0
    except Exception as exc:
        msg = f"{run_time.isoformat()} ERROR {type(exc).__name__}: {exc}\n"
        log_path.open("a", encoding="utf-8").write(msg)
        print(msg, file=sys.stderr, end="")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
