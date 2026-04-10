#!/usr/bin/env python3
"""
YouTube video search via yt-dlp.

Usage:
    python3 scripts/search_youtube.py --query "Claude Code tutorials" --max-results 10
    python3 scripts/search_youtube.py --query "topic" --max-results 5 --min-duration 120 --max-duration 3600

Output: JSON array to stdout, errors/warnings to stderr.
Exit codes: 0=success, 1=no results, 2=yt-dlp error
"""

import argparse
import json
import re
import subprocess
import sys


def slugify(text: str) -> str:
    """Convert title to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")[:60]


def search_youtube(
    query: str,
    max_results: int = 10,
    min_duration: int = 120,
    max_duration: int = 10800,
) -> list[dict]:
    """Search YouTube using yt-dlp and return filtered video list."""
    search_term = f"ytsearch{max_results * 2}:{query}"

    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-download",
        "--flat-playlist",
        "--quiet",
        search_term,
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60
        )
    except subprocess.TimeoutExpired:
        print("ERROR: yt-dlp search timed out", file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError:
        print("ERROR: yt-dlp not found on PATH", file=sys.stderr)
        sys.exit(2)

    if result.returncode != 0 and not result.stdout.strip():
        print(f"ERROR: yt-dlp failed: {result.stderr[:500]}", file=sys.stderr)
        sys.exit(2)

    videos = []
    for line in result.stdout.strip().splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue

        video_id = item.get("id") or item.get("url", "").split("v=")[-1]
        title = item.get("title", "")
        channel = item.get("uploader") or item.get("channel") or ""
        duration = item.get("duration") or 0
        description = item.get("description") or ""

        if not video_id or not title:
            continue

        # Filter by duration
        if min_duration and duration < min_duration:
            continue
        if max_duration and duration > max_duration:
            continue

        # Skip YouTube Shorts URL patterns
        url = f"https://www.youtube.com/watch?v={video_id}"

        videos.append(
            {
                "id": video_id,
                "url": url,
                "title": title,
                "channel": channel,
                "duration": int(duration),
                "duration_str": _format_duration(int(duration)),
                "description": description[:300],
                "slug": slugify(title),
            }
        )

        if len(videos) >= max_results:
            break

    return videos


def _format_duration(seconds: int) -> str:
    """Format seconds as HH:MM:SS or MM:SS."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def main():
    parser = argparse.ArgumentParser(description="Search YouTube via yt-dlp")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument(
        "--max-results", type=int, default=10, help="Max videos to return (default: 10)"
    )
    parser.add_argument(
        "--min-duration",
        type=int,
        default=120,
        help="Min duration in seconds (default: 120)",
    )
    parser.add_argument(
        "--max-duration",
        type=int,
        default=10800,
        help="Max duration in seconds (default: 10800)",
    )
    args = parser.parse_args()

    videos = search_youtube(
        query=args.query,
        max_results=args.max_results,
        min_duration=args.min_duration,
        max_duration=args.max_duration,
    )

    if not videos:
        print("WARNING: No videos found matching criteria", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(videos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
