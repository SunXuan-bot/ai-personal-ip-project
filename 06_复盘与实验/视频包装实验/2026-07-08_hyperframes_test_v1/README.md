# HyperFrames 包装测试 v1

创建时间：2026-07-08  
目的：在不使用 `ffmpeg` 做画面拼接的前提下，先验证 HyperFrames 是否能承担第 1 期 AI 资讯口播的视频包装。

## 方案

- 原始粗剪视频通过符号链接接入：`public/assets/input-video.mp4`
- `public/index.html` 负责全部包装：真人视频框、右侧新闻卡片、底部字幕条、滚动关键词条、GSAP 动效。
- 当前版本不做最终 MP4 导出，因为本机没有 `ffmpeg/ffprobe`，HyperFrames render 也需要底层编码器。

## 当前限制

- 当前测试为了验证浏览器播放，先用 macOS `avconvert` 转了 12 秒 H.264 小段：`transcoded/input-video-12s-h264.m4v`。
- 卡片时间是按文本手工估算，不是精确字幕时间轴。
- 新闻截图、GitHub 页面截图、官方文档截图还没有接入。
- 事实数字仍标记为待复核，不能当作发布定稿。
- 这个版本用于看包装方向，不用于发布。

## 验证目标

1. HyperFrames 是否能正常加载粗剪视频。
2. 真人口播 + 信息卡片 + 字幕条是否能在一个画面里共存。
3. 这种工作台式资讯包装是否比纯 `ffmpeg` 合成更有可塑性。

## 本轮验证结果

时间：2026-07-08

- `npx hyperframes lint . --json`：通过，0 error，0 warning。
- `npx hyperframes validate . --json --timeout 8000`：通过，0 runtime error，0 warning，0 contrast failure。
- `npx hyperframes inspect . --json --at 5,10`：通过，0 error，0 warning。
- Playwright/Chrome 真实预览：通过，视频可播放，`readyState=4`，预览截图已保存为 `preview-browser-5s-final.png`。
- `npx hyperframes render . -o ../test-output.mp4 --fps 30`：已通过。
- `test-output.mp4`：已生成，约 4.9MB，12 秒，1920x1080，H.264 视频 + AAC 音频。

## 关键发现

- HyperFrames 可以承担包装层：信息卡、字幕条、品牌条、时间线动效都可控，明显比纯命令行合成更适合后续迭代。
- 原始粗剪视频是 HEVC + AAC、1080x1920；HyperFrames snapshot 对本地视频抽帧时出现黑屏，但 Chrome 真实预览在 H.264 小段上可以正常显示。
- 后续若要稳定生产，建议把粗剪母版先导出为浏览器友好的 H.264 MP4，再交给 HyperFrames 包装。
- 这里的“转码/编码”不是用 `ffmpeg` 做画面包装，而是视频生产链路里不可避免的底层格式处理。

## 本机编码器状态

- `ffmpeg` 已安装到：`/Users/sunxuan/.local/bin/ffmpeg`。
- `ffprobe` 已安装到：`/Users/sunxuan/.local/bin/ffprobe`。
- HyperFrames doctor 已识别到二者。
