#!/usr/bin/env python3
"""
Extract metadata for a YouTube video.

Tries yt-dlp first (most complete), falls back to yt-dlp search extractor
if direct URL access is blocked (bot detection).

Usage:
    python3 scripts/extract_metadata.py --url "https://www.youtube.com/watch?v=ID"
    python3 scripts/extract_metadata.py --url "https://youtu.be/ID"

Output: JSON to stdout with fields: id, title, channel, channel_url,
        duration, duration_str, upload_date, view_count, description, slug, url

Exit codes:
    0 = success
    1 = video not found or unavailable
    2 = yt-dlp error / all methods failed
"""

import argparse
import json
import re
import subprocess
import sys


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")[:60]


def format_duration(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def extract_video_id(url: str) -> str:
    """Extract video ID from a YouTube URL."""
    patterns = [
        r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    return ""


def parse_yt_dlp_output(data: dict, video_id: str) -> dict:
    """Parse raw yt-dlp JSON into our metadata format."""
    duration = int(data.get("duration") or 0)
    title = data.get("title", "") or ""
    vid_id = data.get("id", video_id)
    return {
        "id": vid_id,
        "title": title,
        "channel": data.get("uploader") or data.get("channel") or "",
        "channel_url": data.get("uploader_url") or data.get("channel_url") or "",
        "duration": duration,
        "duration_str": format_duration(duration),
        "upload_date": data.get("upload_date", "") or "",
        "view_count": data.get("view_count") or 0,
        "description": (data.get("description") or "")[:500],
        "slug": slugify(title),
        "url": f"https://www.youtube.com/watch?v={vid_id}",
    }


def run_yt_dlp(args: list[str], timeout: int = 30) -> tuple[int, str, str]:
    """Run yt-dlp and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["yt-dlp"] + args, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except FileNotFoundError:
        return -1, "", "yt-dlp not found"


def extract_metadata_direct(url: str) -> dict | None:
    """Try direct URL metadata extraction."""
    code, stdout, stderr = run_yt_dlp(
        ["--dump-json", "--no-download", "--quiet", url]
    )
    if code == 0 and stdout.strip():
        try:
            data = json.loads(stdout)
            return parse_yt_dlp_output(data, extract_video_id(url))
        except json.JSONDecodeError:
            pass
    return None


def extract_metadata_via_search(video_id: str) -> dict | None:
    """Fallback: search by video ID using the search extractor (avoids bot detection)."""
    code, stdout, stderr = run_yt_dlp(
        [
            "--dump-json", "--no-download", "--quiet", "--flat-playlist",
            f"ytsearch1:{video_id}"
        ]
    )
    if code == 0:
        for line in stdout.strip().splitlines():
            try:
                data = json.loads(line)
                # Verify this is the right video
                result_id = data.get("id", "")
                if result_id == video_id or video_id in data.get("url", ""):
                    return parse_yt_dlp_output(data, video_id)
            except json.JSONDecodeError:
                continue
    return None


def extract_metadata_minimal(url: str) -> dict:
    """Last resort: return minimal metadata from the URL alone."""
    video_id = extract_video_id(url)
    return {
        "id": video_id,
        "title": f"Video {video_id}",
        "channel": "",
        "channel_url": "",
        "duration": 0,
        "duration_str": "unknown",
        "upload_date": "",
        "view_count": 0,
        "description": "",
        "slug": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "_metadata_incomplete": True,
    }


def extract_metadata(url: str) -> dict:
    """Extract metadata using best available method."""
    video_id = extract_video_id(url)

    if not video_id:
        print(f"ERROR: Could not extract video ID from URL: {url}", file=sys.stderr)
        sys.exit(1)

    # Method 1: Direct URL
    result = extract_metadata_direct(url)
    if result:
        return result

    # Method 2: Search-based fallback (avoids bot detection)
    print("WARNING: Direct metadata fetch blocked, trying search fallback...", file=sys.stderr)
    result = extract_metadata_via_search(video_id)
    if result:
        return result

    # Method 3: Minimal from URL
    print("WARNING: Could not fetch full metadata, using minimal info from URL", file=sys.stderr)
    return extract_metadata_minimal(url)


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube video metadata")
    parser.add_argument("--url", required=True, help="YouTube video URL or video ID")
    args = parser.parse_args()

    metadata = extract_metadata(args.url)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
