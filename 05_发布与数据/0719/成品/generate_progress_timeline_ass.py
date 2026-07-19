from pathlib import Path
from PIL import ImageFont

OUT = Path(__file__).with_name("timeline_progress_timestamps.ass")
FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
FONT_NAME = "Microsoft YaHei"
TITLE_FONT_SIZE = 21
TIME_FONT_SIZE = 15
BAR_H = 68
TIME_Y = 8
TITLE_Y = 33
VIDEO_W = 1920

boundaries = [0, 274, 549, 823, 1097, 1371, 1646, 1917]
segment_times = [0.0, 17.866, 46.600, 69.966, 117.866, 166.000, 223.066, 269.050]
labels = [
    "99元皮肤其实开源",
    "Codex 的安装",
    "效果图要自己生图",
    "重启查看默认皮肤",
    "上传照片让AI换肤",
    "追问整体UI统一",
    "复制提示词继续改",
]
time_labels = ["00:00", "00:18", "00:47", "01:10", "01:58", "02:46", "03:43"]

title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)
time_font = ImageFont.truetype(FONT_PATH, TIME_FONT_SIZE)


def ass_time(seconds: float) -> str:
    seconds = max(0, seconds)
    cs = int(round(seconds * 100))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, c = divmod(rem, 100)
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"


def time_for_x(x: float) -> float:
    for i in range(len(boundaries) - 1):
        left, right = boundaries[i], boundaries[i + 1]
        if x <= right or i == len(boundaries) - 2:
            start, end = segment_times[i], segment_times[i + 1]
            ratio = 0 if right == left else (x - left) / (right - left)
            return start + ratio * (end - start)
    return segment_times[-1]


def title_width(text: str) -> float:
    return title_font.getlength(text)


def time_width(text: str) -> float:
    return time_font.getlength(text)


def dialogue(layer: int, start: float, end: float, style: str, text: str) -> str:
    return f"Dialogue: {layer},{ass_time(start)},{ass_time(end)},{style},,0,0,0,,{text}"


lines = [
    "[Script Info]",
    "ScriptType: v4.00+",
    f"PlayResX: {VIDEO_W}",
    "PlayResY: 1080",
    "WrapStyle: 0",
    "ScaledBorderAndShadow: yes",
    "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    f"Style: TimelineTitle,{FONT_NAME},{TITLE_FONT_SIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
    f"Style: TimelineTitleDark,{FONT_NAME},{TITLE_FONT_SIZE},&H00000000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
    f"Style: TimelineTime,{FONT_NAME},{TIME_FONT_SIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
    f"Style: TimelineTimeDark,{FONT_NAME},{TIME_FONT_SIZE},&H00000000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
    "Style: Shape,Arial,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
    "",
    "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]

end_time = segment_times[-1]
shape = f"m 0 0 l {VIDEO_W} 0 l {VIDEO_W} {BAR_H} l 0 {BAR_H}"
cursor_shape = f"m 0 0 l 6 0 l 6 {BAR_H} l 0 {BAR_H}"
divider_shape = f"m 0 0 l 3 0 l 3 {BAR_H} l 0 {BAR_H}"

lines.append(dialogue(0, 0, end_time, "Shape", r"{\an7\pos(0,0)\p1\c&H000000&}" + shape))

progress_shape = f"m 0 0 l {VIDEO_W} 0 l {VIDEO_W} {BAR_H} l 0 {BAR_H}"
for i in range(len(boundaries) - 1):
    start_x = boundaries[i] - VIDEO_W
    end_x = boundaries[i + 1] - VIDEO_W
    lines.append(
        dialogue(
            1,
            segment_times[i],
            segment_times[i + 1],
            "Shape",
            rf"{{\an7\move({start_x},0,{end_x},0)\p1\c&HFFFFFF&}}{progress_shape}",
        )
    )

for x in boundaries:
    draw_x = min(x, VIDEO_W - 3)
    lines.append(dialogue(2, 0, end_time, "Shape", rf"{{\an7\pos({draw_x},0)\p1\c&HFFFFFF&}}{divider_shape}"))

for x in boundaries:
    draw_x = min(x, VIDEO_W - 3)
    lines.append(dialogue(4, time_for_x(draw_x), end_time, "Shape", rf"{{\an7\pos({draw_x},0)\p1\c&H000000&}}{divider_shape}"))

for i in range(len(boundaries) - 1):
    lines.append(
        dialogue(
            5,
            segment_times[i],
            segment_times[i + 1],
            "Shape",
            rf"{{\an7\move({boundaries[i]},0,{min(boundaries[i + 1], VIDEO_W - 6)},0)\p1\c&H66D1FF&}}{cursor_shape}",
        )
    )

title_starts = []
time_starts = []
for i, label in enumerate(labels):
    cell_left, cell_right = boundaries[i], boundaries[i + 1]
    title_x = cell_left + (cell_right - cell_left - title_width(label)) / 2
    time_x = cell_left + (cell_right - cell_left - time_width(time_labels[i])) / 2
    title_starts.append(title_x)
    time_starts.append(time_x)
    lines.append(dialogue(3, 0, end_time, "TimelineTime", rf"{{\an7\pos({time_x:.1f},{TIME_Y})}}{time_labels[i]}"))
    lines.append(dialogue(3, 0, end_time, "TimelineTitle", rf"{{\an7\pos({title_x:.1f},{TITLE_Y})}}{label}"))

def add_reveal_text(label: str, start_x: float, y: int, width_fn, style: str) -> None:
    reveal_points = []
    prefix = ""
    for ch in label:
        prefix += ch
        if ch.isspace():
            continue
        ch_end_x = start_x + width_fn(prefix)
        reveal_points.append((time_for_x(ch_end_x), ch_end_x))

    for idx, (start_t, clip_x) in enumerate(reveal_points):
        end_t = reveal_points[idx + 1][0] if idx + 1 < len(reveal_points) else end_time
        if end_t <= start_t:
            continue
        lines.append(
            dialogue(
                6,
                start_t,
                end_t,
                style,
                rf"{{\an7\clip(0,0,{clip_x:.1f},{BAR_H})\pos({start_x:.1f},{y})}}{label}",
            )
        )


for label, start_x in zip(labels, title_starts):
    add_reveal_text(label, start_x, TITLE_Y, title_width, "TimelineTitleDark")

for label, start_x in zip(time_labels, time_starts):
    add_reveal_text(label, start_x, TIME_Y, time_width, "TimelineTimeDark")

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(OUT)
