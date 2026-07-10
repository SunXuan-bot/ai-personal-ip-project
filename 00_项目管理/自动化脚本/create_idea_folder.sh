#!/usr/bin/env bash
set -euo pipefail

TITLE="${1:-}"
RAW="${2:-}"

if [[ -z "$TITLE" ]]; then
  echo "用法: $0 \"短标题\" \"原始想法内容\""
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DATE="$(date '+%Y-%m-%d')"
SAFE_TITLE="$(printf '%s' "$TITLE" | perl -CS -Mutf8 -pe 's/[\/:[:space:]]+/_/g; s/[^\p{Han}\p{L}\p{N}_.-]//g')"
DIR="$ROOT/03_选题库/点子库/${DATE}_${SAFE_TITLE}"

mkdir -p "$DIR/素材"

cat > "$DIR/原始输入.md" <<EOF
# 原始输入：$TITLE

日期：$DATE
来源：Hermes / 用户临时记录

## 原始想法

$RAW
EOF

cat > "$DIR/点子卡.md" <<EOF
# 点子卡：$TITLE

## 基本信息

- 日期：$DATE
- 标题：$TITLE
- 来源：Hermes / 用户临时记录
- 当前状态：待整理
- 对应栏目：待判断

## 原始想法

$RAW

## 为什么值得做

- 待 Codex 整理

## 可能的视频角度

1. 待 Codex 整理

## 需要补的来源 / 素材

- 待补

## 下一步

- 待 Codex 拆解
EOF

cat > "$DIR/使用记录.md" <<EOF
# 使用记录：$TITLE

## $DATE

- 由脚本创建点子文件夹。
- 当前状态：待整理。

| 日期 | 动作 | 文件 / 链接 | 结果 |
| --- | --- | --- | --- |
| $DATE | 创建点子 | $DIR | 待 Codex 整理 |
EOF

echo "已创建: $DIR"
