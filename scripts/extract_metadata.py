#!/usr/bin/env python3
"""
Extract metadata for a YouTube video via YouTube Data API v3.

Requires YOUTUBE_API_KEY environment variable (or --api-key argument).
Get a free key at: https://console.cloud.google.com/apis/library/youtube.googleapis.com
Cost: 1 quota unit per call (10,000 free units/day).

Usage:
    python3 scripts/extract_metadata.py --url "https://www.youtube.com/watch?v=ID"
    python3 scripts/extract_metadata.py --url "https://youtu.be/ID"

Output: JSON to stdout with fields: id, title, channel, channel_url,
        duration, duration_str, upload_date, view_count, description, slug, url

Exit codes:
    0 = success
    1 = video not found or unavailable
    2 = API error
    3 = API key missing
"""

import argparse
import json
import os
import re
import sys

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: bash scripts/setup.sh", file=sys.stderr)
    sys.exit(2)

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


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


def parse_iso8601_duration(duration_str: str) -> int:
    """Parse ISO 8601 duration (e.g. PT1H2M3S) into total seconds."""
    if not duration_str:
        return 0
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_str)
    if not m:
        return 0
    return int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)


def extract_video_id(url: str) -> str:
    """Extract video ID from a YouTube URL, or return as-is if already an 11-char ID."""
    patterns = [
        r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    return ""


def extract_metadata(url: str, api_key: str | None = None) -> dict:
    """Fetch video metadata from YouTube Data API v3 videos.list."""
    video_id = extract_video_id(url)
    if not video_id:
        print(f"ERROR: Could not extract video ID from: {url}", file=sys.stderr)
        sys.exit(1)

    if not api_key:
        api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print(
            "ERROR: YOUTUBE_API_KEY not set.\n"
            "Get a free key at: https://console.cloud.google.com/apis/library/youtube.googleapis.com\n"
            "Then: export YOUTUBE_API_KEY=your_key_here",
            file=sys.stderr,
        )
        sys.exit(3)

    try:
        resp = requests.get(
            f"{YOUTUBE_API_BASE}/videos",
            params={
                "part": "snippet,contentDetails,statistics",
                "id": video_id,
                "key": api_key,
            },
            timeout=15,
        )
    except requests.RequestException as e:
        print(f"ERROR: YouTube API request failed: {e}", file=sys.stderr)
        sys.exit(2)

    if resp.status_code == 403:
        try:
            reason = resp.json().get("error", {}).get("errors", [{}])[0].get("reason", "")
        except Exception:
            reason = ""
        if reason in ("quotaExceeded", "dailyLimitExceeded"):
            print("ERROR: YouTube Data API daily quota exceeded. Resets at midnight Pacific Time.", file=sys.stderr)
        else:
            print(f"ERROR: YouTube API returned 403: {resp.text[:300]}", file=sys.stderr)
        sys.exit(2)

    if resp.status_code != 200:
        print(f"ERROR: YouTube API returned {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
        sys.exit(2)

    items = resp.json().get("items", [])
    if not items:
        print(f"ERROR: Video {video_id} not found or unavailable", file=sys.stderr)
        sys.exit(1)

    item = items[0]
    snippet = item.get("snippet", {})
    content_details = item.get("contentDetails", {})
    stats = item.get("statistics", {})

    duration = parse_iso8601_duration(content_details.get("duration", ""))
    title = snippet.get("title", "")
    channel_id = snippet.get("channelId", "")

    return {
        "id": video_id,
        "title": title,
        "channel": snippet.get("channelTitle", ""),
        "channel_url": f"https://www.youtube.com/channel/{channel_id}" if channel_id else "",
        "duration": duration,
        "duration_str": format_duration(duration),
        "upload_date": snippet.get("publishedAt", "")[:10].replace("-", ""),
        "view_count": int(stats.get("viewCount", 0) or 0),
        "description": snippet.get("description", "")[:500],
        "slug": slugify(title),
        "url": f"https://www.youtube.com/watch?v={video_id}",
    }


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube video metadata via YouTube Data API v3")
    parser.add_argument("--url", required=True, help="YouTube video URL or video ID")
    parser.add_argument("--api-key", default=None, help="YouTube Data API v3 key (overrides YOUTUBE_API_KEY env var)")
    args = parser.parse_args()

    metadata = extract_metadata(args.url, args.api_key)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
