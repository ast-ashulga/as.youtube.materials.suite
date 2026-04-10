#!/usr/bin/env python3
"""
YouTube video search via YouTube Data API v3.

Requires YOUTUBE_API_KEY environment variable (or --api-key argument).
Get a free key at: https://console.cloud.google.com/apis/library/youtube.googleapis.com
Free quota: 10,000 units/day (~100 searches/day).

Usage:
    python3 scripts/search_youtube.py --query "Claude Code" --max-results 10
    python3 scripts/search_youtube.py --query "topic" --max-results 5 --min-duration 120 --max-duration 3600

Output: JSON array to stdout, errors/warnings to stderr.
Exit codes: 0=success, 1=no results, 2=API error, 3=API key missing
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


def _format_duration(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def _parse_iso8601_duration(duration_str: str) -> int:
    """Parse ISO 8601 duration (e.g. PT1H2M3S) into total seconds."""
    if not duration_str:
        return 0
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_str)
    if not m:
        return 0
    return int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)


def search_youtube(
    query: str,
    max_results: int = 10,
    min_duration: int = 120,
    max_duration: int = 10800,
    api_key: str | None = None,
) -> list[dict]:
    """Search YouTube using YouTube Data API v3 and return filtered video list."""
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

    # Step 1: search.list — returns video IDs and basic snippet (costs 100 quota units)
    # Fetch 3x the requested count to have enough after duration filtering
    fetch_count = min(50, max_results * 3)

    try:
        resp = requests.get(
            f"{YOUTUBE_API_BASE}/search",
            params={
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": fetch_count,
                "key": api_key,
            },
            timeout=15,
        )
    except requests.RequestException as e:
        print(f"ERROR: YouTube API search request failed: {e}", file=sys.stderr)
        sys.exit(2)

    if resp.status_code == 403:
        try:
            reason = resp.json().get("error", {}).get("errors", [{}])[0].get("reason", "")
        except Exception:
            reason = ""
        if reason in ("quotaExceeded", "dailyLimitExceeded"):
            print(
                "ERROR: YouTube Data API daily quota exceeded (10,000 units/day). "
                "Quota resets at midnight Pacific Time.",
                file=sys.stderr,
            )
        else:
            print(f"ERROR: YouTube API returned 403 (check API key and enabled APIs): {resp.text[:300]}", file=sys.stderr)
        sys.exit(2)

    if resp.status_code != 200:
        print(f"ERROR: YouTube API search returned {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
        sys.exit(2)

    items = resp.json().get("items", [])
    video_ids = [
        item["id"]["videoId"]
        for item in items
        if item.get("id", {}).get("kind") == "youtube#video"
    ]
    if not video_ids:
        return []

    # Step 2: videos.list — get exact duration and stats for all IDs in one batch (costs 1 quota unit)
    try:
        resp2 = requests.get(
            f"{YOUTUBE_API_BASE}/videos",
            params={
                "part": "snippet,contentDetails,statistics",
                "id": ",".join(video_ids),
                "key": api_key,
            },
            timeout=15,
        )
    except requests.RequestException as e:
        print(f"ERROR: YouTube API videos request failed: {e}", file=sys.stderr)
        sys.exit(2)

    if resp2.status_code != 200:
        print(f"ERROR: YouTube API videos returned {resp2.status_code}: {resp2.text[:300]}", file=sys.stderr)
        sys.exit(2)

    video_details = {v["id"]: v for v in resp2.json().get("items", [])}

    # Step 3: Build result list with duration filtering, preserving search rank order
    results = []
    for vid_id in video_ids:
        detail = video_details.get(vid_id)
        if not detail:
            continue

        snippet = detail.get("snippet", {})
        content_details = detail.get("contentDetails", {})
        stats = detail.get("statistics", {})

        duration_secs = _parse_iso8601_duration(content_details.get("duration", ""))

        if min_duration and duration_secs < min_duration:
            continue
        if max_duration and duration_secs > max_duration:
            continue

        title = snippet.get("title", "")
        results.append({
            "id": vid_id,
            "url": f"https://www.youtube.com/watch?v={vid_id}",
            "title": title,
            "channel": snippet.get("channelTitle", ""),
            "duration": duration_secs,
            "duration_str": _format_duration(duration_secs),
            "description": snippet.get("description", "")[:300],
            "slug": slugify(title),
            "view_count": int(stats.get("viewCount", 0) or 0),
            "publish_date": snippet.get("publishedAt", "")[:10],
        })

        if len(results) >= max_results:
            break

    return results


def main():
    parser = argparse.ArgumentParser(description="Search YouTube via YouTube Data API v3")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--max-results", type=int, default=10, help="Max videos to return (default: 10)")
    parser.add_argument("--min-duration", type=int, default=120, help="Min duration in seconds (default: 120)")
    parser.add_argument("--max-duration", type=int, default=10800, help="Max duration in seconds (default: 10800)")
    parser.add_argument("--api-key", default=None, help="YouTube Data API v3 key (overrides YOUTUBE_API_KEY env var)")
    args = parser.parse_args()

    videos = search_youtube(
        query=args.query,
        max_results=args.max_results,
        min_duration=args.min_duration,
        max_duration=args.max_duration,
        api_key=args.api_key,
    )

    if not videos:
        print("WARNING: No videos found matching criteria", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(videos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
