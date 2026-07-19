import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path

try:
    from PIL import ImageFont
except ImportError as exc:
    raise SystemExit("Pillow is required. Install it with: pip install pillow") from exc


DEFAULT_FONT_PATHS = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]


def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(
            "Command failed:\n"
            + " ".join(str(x) for x in cmd)
            + "\n\nSTDOUT:\n"
            + result.stdout
            + "\nSTDERR:\n"
            + result.stderr
        )
    return result.stdout


def parse_time(value):
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", ".")
    parts = text.split(":")
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    return float(text)


def ass_time(seconds):
    seconds = max(0.0, float(seconds))
    centiseconds = int(round(seconds * 100))
    hours, rem = divmod(centiseconds, 360000)
    minutes, rem = divmod(rem, 6000)
    secs, cs = divmod(rem, 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{cs:02d}"


def display_time(seconds):
    seconds = int(round(seconds))
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def ffprobe(path):
    data = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate,duration",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ]
    )
    info = json.loads(data)
    stream = info["streams"][0]
    duration = float(stream.get("duration") or info["format"]["duration"])
    return int(stream["width"]), int(stream["height"]), duration


def load_chapters(path, duration):
    chapters = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(chapters, list) or not chapters:
        raise SystemExit("chapters JSON must be a non-empty array")

    parsed = []
    for item in chapters:
        if "title" not in item:
            raise SystemExit("each chapter needs a title")
        start = parse_time(item.get("start", 0))
        title = str(item["title"]).strip()
        if not title:
            raise SystemExit("chapter title cannot be empty")
        parsed.append({"start": start, "title": title})

    parsed.sort(key=lambda x: x["start"])
    if parsed[0]["start"] > 0.25:
        parsed.insert(0, {"start": 0.0, "title": parsed[0]["title"]})
    else:
        parsed[0]["start"] = 0.0

    for prev, curr in zip(parsed, parsed[1:]):
        if curr["start"] <= prev["start"]:
            raise SystemExit("chapter starts must be strictly increasing")
    if parsed[-1]["start"] >= duration:
        raise SystemExit("last chapter start must be before video end")
    return parsed


def choose_font(path_arg):
    candidates = [path_arg] if path_arg else []
    candidates.extend(DEFAULT_FONT_PATHS)
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise SystemExit("No usable font found. Pass --font-file explicitly.")


def ass_dialogue(layer, start, end, style, text):
    return f"Dialogue: {layer},{ass_time(start)},{ass_time(end)},{style},,0,0,0,,{text}"


def build_ass(
    ass_path,
    chapters,
    width,
    height,
    duration,
    font_file,
    font_name,
    bar_height,
    title_font_size,
    time_font_size,
):
    scale = width / 1920
    bar_h = int(round(bar_height * scale))
    title_size = max(14, int(round(title_font_size * scale)))
    time_size = max(10, int(round(time_font_size * scale)))
    time_y = max(4, int(round(8 * scale)))
    title_y = max(time_y + time_size + 5, int(round(33 * scale)))

    title_font = ImageFont.truetype(font_file, title_size)
    time_font = ImageFont.truetype(font_file, time_size)

    starts = [c["start"] for c in chapters] + [duration]
    cell_count = len(chapters)
    boundaries = [round(i * width / cell_count) for i in range(cell_count + 1)]
    boundaries[-1] = width

    def title_width(text):
        return title_font.getlength(text)

    def time_width(text):
        return time_font.getlength(text)

    def time_for_x(x):
        for i in range(cell_count):
            left, right = boundaries[i], boundaries[i + 1]
            if x <= right or i == cell_count - 1:
                start, end = starts[i], starts[i + 1]
                ratio = 0 if right == left else (x - left) / (right - left)
                return start + ratio * (end - start)
        return duration

    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {width}",
        f"PlayResY: {height}",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: TimelineTitle,{font_name},{title_size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        f"Style: TimelineTitleDark,{font_name},{title_size},&H00000000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        f"Style: TimelineTime,{font_name},{time_size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        f"Style: TimelineTimeDark,{font_name},{time_size},&H00000000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        "Style: Shape,Arial,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    full_shape = f"m 0 0 l {width} 0 l {width} {bar_h} l 0 {bar_h}"
    divider_shape = f"m 0 0 l {max(2, round(3 * scale))} 0 l {max(2, round(3 * scale))} {bar_h} l 0 {bar_h}"
    cursor_w = max(4, round(6 * scale))
    cursor_shape = f"m 0 0 l {cursor_w} 0 l {cursor_w} {bar_h} l 0 {bar_h}"

    lines.append(ass_dialogue(0, 0, duration, "Shape", r"{\an7\pos(0,0)\p1\c&H000000&}" + full_shape))

    for i in range(cell_count):
        start_x = boundaries[i] - width
        end_x = boundaries[i + 1] - width
        lines.append(
            ass_dialogue(
                1,
                starts[i],
                starts[i + 1],
                "Shape",
                rf"{{\an7\move({start_x},0,{end_x},0)\p1\c&HFFFFFF&}}{full_shape}",
            )
        )

    for x in boundaries:
        draw_x = min(x, width - max(2, round(3 * scale)))
        lines.append(ass_dialogue(2, 0, duration, "Shape", rf"{{\an7\pos({draw_x},0)\p1\c&HFFFFFF&}}{divider_shape}"))
        lines.append(ass_dialogue(4, time_for_x(draw_x), duration, "Shape", rf"{{\an7\pos({draw_x},0)\p1\c&H000000&}}{divider_shape}"))

    for i in range(cell_count):
        lines.append(
            ass_dialogue(
                5,
                starts[i],
                starts[i + 1],
                "Shape",
                rf"{{\an7\move({boundaries[i]},0,{min(boundaries[i + 1], width - cursor_w)},0)\p1\c&H66D1FF&}}{cursor_shape}",
            )
        )

    title_starts = []
    time_starts = []
    time_labels = [display_time(c["start"]) for c in chapters]
    for i, chapter in enumerate(chapters):
        cell_left, cell_right = boundaries[i], boundaries[i + 1]
        title = chapter["title"]
        time_label = time_labels[i]
        title_x = cell_left + (cell_right - cell_left - title_width(title)) / 2
        time_x = cell_left + (cell_right - cell_left - time_width(time_label)) / 2
        title_starts.append(title_x)
        time_starts.append(time_x)
        lines.append(ass_dialogue(3, 0, duration, "TimelineTime", rf"{{\an7\pos({time_x:.1f},{time_y})}}{time_label}"))
        lines.append(ass_dialogue(3, 0, duration, "TimelineTitle", rf"{{\an7\pos({title_x:.1f},{title_y})}}{title}"))

    def add_reveal_text(text, start_x, y, width_fn, style):
        reveal_points = []
        prefix = ""
        for ch in text:
            prefix += ch
            if ch.isspace():
                continue
            ch_end_x = start_x + width_fn(prefix)
            reveal_points.append((time_for_x(ch_end_x), ch_end_x))
        for idx, (start_t, clip_x) in enumerate(reveal_points):
            end_t = reveal_points[idx + 1][0] if idx + 1 < len(reveal_points) else duration
            if end_t <= start_t:
                continue
            lines.append(
                ass_dialogue(
                    6,
                    start_t,
                    end_t,
                    style,
                    rf"{{\an7\clip(0,0,{clip_x:.1f},{bar_h})\pos({start_x:.1f},{y})}}{text}",
                )
            )

    for chapter, start_x in zip(chapters, title_starts):
        add_reveal_text(chapter["title"], start_x, title_y, title_width, "TimelineTitleDark")
    for label, start_x in zip(time_labels, time_starts):
        add_reveal_text(label, start_x, time_y, time_width, "TimelineTimeDark")

    ass_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render(args):
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    width, height, duration = ffprobe(input_path)
    chapters = load_chapters(args.chapters, duration)
    font_file = choose_font(args.font_file)
    ass_path = output_path.with_suffix(".timestamps.ass")

    build_ass(
        ass_path,
        chapters,
        width,
        height,
        duration,
        font_file,
        args.font_name,
        args.bar_height,
        args.title_font_size,
        args.time_font_size,
    )

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg not found in PATH")

    cmd = [
        ffmpeg,
        "-hide_banner",
        "-y",
        "-i",
        str(input_path),
        "-vf",
        f"ass='{ass_path.name}'",
        "-map",
        "0:v:0",
        "-map",
        "0:a?",
        "-c:v",
        "libx264",
        "-preset",
        args.preset,
        "-crf",
        str(args.crf),
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        args.audio_bitrate,
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    run(cmd, cwd=output_path.parent)
    print(output_path)


def main():
    parser = argparse.ArgumentParser(description="Render a chapter timestamp progress bar onto a video.")
    parser.add_argument("--input", required=True, help="Input video path")
    parser.add_argument("--chapters", required=True, help="JSON array with start/title chapters")
    parser.add_argument("--output", required=True, help="Output MP4 path")
    parser.add_argument("--font-file", default=None, help="Font file path, defaults to Microsoft YaHei on Windows")
    parser.add_argument("--font-name", default="Microsoft YaHei", help="ASS font family name")
    parser.add_argument("--bar-height", type=int, default=68, help="Base bar height for 1920px wide video")
    parser.add_argument("--title-font-size", type=int, default=21, help="Base title font size for 1920px wide video")
    parser.add_argument("--time-font-size", type=int, default=15, help="Base timestamp font size for 1920px wide video")
    parser.add_argument("--crf", type=int, default=20, help="libx264 CRF quality")
    parser.add_argument("--preset", default="veryfast", help="libx264 preset")
    parser.add_argument("--audio-bitrate", default="192k", help="AAC audio bitrate")
    args = parser.parse_args()
    render(args)


if __name__ == "__main__":
    main()
