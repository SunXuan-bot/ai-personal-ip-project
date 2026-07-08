# 2026-07-08 竖屏包装 v2 素材台账

## 输入素材

| 类型 | 路径 | 说明 |
| --- | --- | --- |
| 原始剪映导出视频 | `../../02_素材与资料/测试视频/7月8日/7月8日.mp4` | 已带剪映字幕，HEVC 60fps，97.20 秒 |
| 剪映字幕文件 | `../../02_素材与资料/测试视频/7月8日/7月8日.srt` | 用于生成新闻分段时间轴，不再由 HyperFrames 显示字幕 |
| H.264 工作副本 | `public/assets/video/input-with-jianying-subtitles-h264.mp4` | 转为 H.264 30fps，便于浏览器预览和 HyperFrames 渲染 |

## 结构化数据

| 文件 | 说明 |
| --- | --- |
| `public/assets/data/jianying-subtitles.srt` | 剪映字幕副本 |
| `public/assets/data/srt-cues.json` | 从 SRT 解析出的 53 条字幕 cue |
| `public/assets/data/news_segments.json` | 基于 SRT 生成的新闻分段时间轴 |

## 公开网页截图

| 素材 | 来源 | 状态 | 用途 |
| --- | --- | --- | --- |
| `public/assets/screenshots/github-deepcode-cli.png` | https://github.com/lessweb/deepcode-cli | 已截图 | Deep Code 新闻画中画 |
| `public/assets/screenshots/github-officecli.png` | https://github.com/iOfficeAI/OfficeCLI | 已截图 | OfficeCLI 新闻画中画 |
| `public/assets/screenshots/aliyun-fun-asr.png` | https://help.aliyun.com/zh/model-studio/fun-asr | 不采用 | 页面返回 404，不作为素材使用 |

## 动态数据核验

时间：2026-07-08  
方式：GitHub 公共 API，未登录 GitHub CLI。

| 项目 | API 结果 | 备注 |
| --- | --- | --- |
| `lessweb/deepcode-cli` | 1699 stars | 口播中的 `1600+` 仍成立 |
| `iOfficeAI/OfficeCLI` | 10525 stars | 口播中的 `8900+` 已偏旧，包装卡用 `10k+` 更稳 |

## 边界说明

- 本版不下载第三方视频素材。
- 本版不把 AI 生图伪装成真实新闻图。
- 本版不覆盖剪映字幕，只使用 SRT 作为包装时间轴依据。
- Fun-ASR 的公开截图暂未找到稳定页面，本版先做数据卡，后续补官方页面或公众号截图。
