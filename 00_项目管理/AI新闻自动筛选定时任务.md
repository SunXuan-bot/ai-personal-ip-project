# AI 新闻自动筛选定时任务

更新日期：2026-07-09

## 目标

每天自动生成两次 AI 新闻候选筛选稿：

- 上午 10:00
- 下午 17:00

用途：让用户每天反馈“哪些像、哪些不像、哪些不够大、哪些不好讲”，持续训练 AI 资讯选择标准。

## 输出位置

```text
04_脚本与内容/AI资讯日更/自动筛选/
```

说明：由于 macOS 对 Desktop 目录有隐私权限限制，launchd 实际写入：

```text
~/.codex/automations/ai-news-scan/output/
```

项目里的 `自动筛选/` 是指向该输出目录的入口。

文件命名：

```text
YYYY-MM-DD_1000_AI新闻候选筛选.md
YYYY-MM-DD_1700_AI新闻候选筛选.md
```

## 自动筛选逻辑

脚本会：

1. 调用 AI HOT 公开精选接口，拉最近 24 小时精选条目。
2. 按当前栏目标准初筛：
   - 是否 AI 圈当天关注的大事。
   - 是否和普通 AI 学习者、创作者、小团队有关。
   - 是否能快速核验。
   - 是否能 10-20 秒讲清楚。
   - 是否可能有强关联官方视频 / Demo / 官网截图。
3. 输出建议入选 5-6 条和备选池。
4. 给每条新闻留出用户反馈区。

## 本机文件

- 脚本：`00_项目管理/自动化脚本/ai_news_scan.py`
- launchd 配置：`00_项目管理/自动化脚本/com.sunxuan.ai-news-scan.plist`
- launchd 运行副本：`~/.codex/automations/ai-news-scan/ai_news_scan.py`
- 日志：`~/.codex/automations/ai-news-scan/logs/`

## macOS 定时任务

实际加载位置：

```text
~/Library/LaunchAgents/com.sunxuan.ai-news-scan.plist
```

查看状态：

```bash
launchctl print gui/$(id -u)/com.sunxuan.ai-news-scan
```

手动触发：

```bash
launchctl kickstart -k gui/$(id -u)/com.sunxuan.ai-news-scan
```

卸载：

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.sunxuan.ai-news-scan.plist
```

## 边界

- 这只是自动生成候选稿，不会自动发布、不会发消息、不会下载视频素材。
- 候选稿仍需要用户反馈和 Codex 二次判断。
- 如果 AI HOT 接口不可用，脚本会写入日志，但不会编造新闻。
