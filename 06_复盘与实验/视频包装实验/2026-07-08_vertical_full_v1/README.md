# HyperFrames 竖屏完整测试 v1

创建时间：2026-07-08  
目标：用完整 97 秒粗剪视频生成 1080x1920 竖屏包装版，先看整体效果。

## 输入

- 原始粗剪：`../../02_素材与资料/测试视频/粗剪测试视频.mp4`
- 原片信息：HEVC + AAC，1080x1920，60fps，约 97.27 秒。

## 输出

- Composition：`public/index.html`
- 目标输出：`output-vertical-full-v1.mp4`
- 已生成输出：`output-vertical-full-v1.mp4`

## 验证结果

- HyperFrames lint：通过。
- HyperFrames validate：通过，无 runtime error；存在少量对比度提示，来自半透明字幕层与视频画面采样。
- HyperFrames inspect：通过，无遮挡/溢出错误。
- Snapshot：已生成 6 张关键帧，见 `public/snapshots/`。
- Render：已完成，渲染耗时约 1 分 43 秒。
- 输出文件：约 67MB，97.30 秒。
- 视频流：H.264，1080x1920，30fps。
- 音频流：AAC，97.30 秒。

## 说明

- 本版先做整体包装效果，不做逐字精准字幕。
- 新闻截图、真实来源截图和生图素材还未接入。
- 字幕时间轴按录制文本粗对齐，后续需要基于音频重校。
