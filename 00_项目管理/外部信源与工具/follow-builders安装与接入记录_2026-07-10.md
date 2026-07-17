# Follow Builders 安装与接入记录

更新日期：2026-07-10

## 结论

已安装 `zarazhangrui/follow-builders`，作为 AI 资讯日更的补充信源。

它和 AI HOT 的分工：

- AI HOT：更适合抓当天已经整理好的 AI 新闻和产品更新。
- Follow Builders：更适合从 AI builder 的 X 动态、播客和官方博客里挖一手线索、观点角度和主新闻背景。

## 安装位置

```text
~/.codex/skills/follow-builders
```

本地配置：

```text
~/.follow-builders/config.json
```

当前配置为中文、按需读取、`stdout` 输出；没有配置 Telegram / Email 自动推送。

## 本机验证

执行位置：

```text
~/.codex/skills/follow-builders/scripts
```

验证命令：

```bash
npm install
node prepare-digest.js
```

2026-07-10 验证结果：

- `status`: `ok`
- feed 生成时间：`2026-07-10T07:27:50.773Z`
- X builders：19
- X tweets：44
- podcast episodes：1
- blog posts：0
- 非致命错误：`@claudeai` 抓取返回 `HTTP 402`

## 已接入的自动筛选脚本

脚本：

```text
00_项目管理/自动化脚本/ai_news_scan.py
```

运行副本：

```text
~/.codex/automations/ai-news-scan/ai_news_scan.py
```

2026-07-10 临时验证结果：

```text
items=66
follow_builders=41
```

生成稿新增：

- `本次信源状态`
- `信源：AI HOT / Follow Builders`
- `Follow Builders 线索池`

## 使用边界

- Follow Builders 中的 X 内容只作为线索，不等同于官方新闻。
- 正式口播前仍需回源核验，优先找到官方公告、博客、GitHub、产品页或原始视频。
- 播客更适合做观点背景和选题角度，不一定适合当天快讯。
- 官方博客条目可信度更高，但仍要确认发布日期和原文事实。
