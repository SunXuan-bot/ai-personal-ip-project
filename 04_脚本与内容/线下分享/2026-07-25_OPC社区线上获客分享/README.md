# OPC 社区线上获客分享

## 当前版本

### 1. 原始绿色版（保留未修改）

- 目录：`output/opc-business-sharing-theme01-v3-green-editable/`
- HTML：`output/opc-business-sharing-theme01-v3-green-editable/ppt/index.html`

### 2. Theme07 绿色优化版

- 目录：`output/opc-business-sharing-theme07-green-refined/`
- HTML：`output/opc-business-sharing-theme07-green-refined/ppt/index.html`
- 特点：冷白绿色、版式克制、9 页、适合作为正式分享主版本。

### 3. Theme11 高能增长版

- 目录：`output/opc-business-sharing-theme11-growth-editorial/`
- HTML：`output/opc-business-sharing-theme11-growth-editorial/ppt/index.html`
- 特点：橙黑增长风、排版与绿色版明显不同、9 页、适合强调增长与成交逻辑。

两个新版本互不覆盖，原始版本也继续保留。跨设备使用时请拉取完整目录，不要只单独下载 `index.html`，否则相对路径下的图片和二维码会缺失。

## 视频素材

优先提供本地 MP4 文件。演示稿内嵌视频建议统一使用：

- 视频编码：H.264
- 音频编码：AAC
- 像素格式：`yuv420p`
- 文件优化：`faststart`

如果本地原片已经没有，也可以提供抖音或视频号的公开链接。我可以先尝试提取成可离线播放的本地 MP4，再放进 HTML；不建议把平台页面或在线播放地址直接嵌入演示稿，因为登录、反盗链、网络和平台页面变化都会影响现场播放。

提供视频时请同时注明：放在哪一页、是否需要裁切、从哪一秒开始、是否保留声音。

## 首尾视觉状态

- 首页当前使用用户提供的高清真实人物照片。
- 尾页先使用原始微信二维码，二维码作为独立素材叠放，能够正常识别。
- `image2` 生图尚未执行：当前运行环境没有内置 `image_gen`，也没有配置 `OPENAI_API_KEY`。这不影响两版 HTML 使用，但如果必须补做 AI 生成的首尾背景，需要先恢复可用的 `image2` 调用环境。

## 本机预览

- Theme07 绿色优化版：`http://127.0.0.1:5533/`
- Theme11 高能增长版：`http://127.0.0.1:5532/`

预览服务只在当前电脑和当前进程运行。换电脑后先执行 `git pull`，再打开对应 `ppt/index.html`；需要在线编辑或导出 PDF/PPTX 时，重新启动 Dashi PPT 预览服务。
