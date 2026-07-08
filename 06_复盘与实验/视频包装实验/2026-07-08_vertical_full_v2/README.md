# HyperFrames 竖屏完整测试 v2

创建时间：2026-07-08  
目标：基于用户反馈优化 v1 包装，验证“剪映字幕 + HyperFrames 标题/素材包装”的分工。

## 输入

- 剪映导出视频：`../../02_素材与资料/测试视频/7月8日/7月8日.mp4`
- 剪映字幕：`../../02_素材与资料/测试视频/7月8日/7月8日.srt`

## 本版修改

- 保留左上角账号名。
- 右上角从 `AI NEWS 01` 改为 `2026.07.08`。
- 保留底部黄色关键词栏。
- 不再生成 HyperFrames 字幕层，直接使用视频里已有剪映字幕。
- 使用 SRT 生成 `news_segments.json`，标题卡时间按真实字幕起点对齐。
- 标题卡改成短卡，自适应文字内容，减少对头发和脸部的遮挡。
- 标题文字采用逐词闪出动效，背板轻微淡入。
- Deep Code 和 OfficeCLI 接入 GitHub 页面截图；Fun-ASR 暂用数据卡。

## 输出

- Composition：`public/index.html`
- H.264 工作视频：`public/assets/video/input-with-jianying-subtitles-h264.mp4`
- 分段数据：`public/assets/data/news_segments.json`
- 素材台账：`visual_assets.md`
- 抽帧检查：`public/snapshots/contact-sheet.jpg`
- 已生成输出：`output-vertical-full-v2.mp4`

## 验证结果

- HyperFrames lint：通过，0 error，0 warning。
- HyperFrames validate：通过，无 runtime warning；日期黄底黑字存在自动对比度采样误报，抽帧肉眼检查正常。
- HyperFrames inspect：通过，0 layout issue。
- Snapshot：已生成 7 张关键帧和 contact sheet。
- Render：已完成，渲染耗时约 1 分 39 秒。
- 输出文件：约 144MB，97.24 秒。
- 视频流：H.264，1080x1920，30fps。
- 音频流：AAC，97.24 秒。

## 抽帧观察

- 标题卡已从 v1 的大卡片改为短卡片，没有明显压住头发。
- 剪映字幕位于画面中下部，与底部黄色关键词栏没有明显冲突。
- 底部关键词栏保留，并按当前新闻高亮。
- GitHub 截图在竖屏里可提供来源感，但页面细节不可完全阅读；后续如果要更强信息传达，应做局部放大或手动裁重点区域。
- Fun-ASR 暂无稳定官方页面截图，本版使用数据卡替代。

## 遗留问题

- 剪映字幕本身有 ASR 误识别，例如 `deepcode官方文档`、`Gethub/gitub`、`cloud code`、`from ASR`。本版不覆盖字幕，因此这些错误仍在视频画面中。
- Claude Code、Hacker News / 研究文章、Fun-ASR 官方来源截图尚未全部补齐。
- 如果本版要作为发布版，建议先在剪映中修正字幕后重新导出，再用同一套 v2 包装重新渲染。
