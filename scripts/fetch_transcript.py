#!/usr/bin/env python3
"""
Fetch transcript for a YouTube video using youtube-transcript-api v1.x.

Usage:
    python3 scripts/fetch_transcript.py --video-id WSPChlfxJyA
    python3 scripts/fetch_transcript.py --video-id WSPChlfxJyA --lang en
    python3 scripts/fetch_transcript.py --video-id WSPChlfxJyA --output /path/to/file.txt

Output:
    - Transcript text to stdout (or --output file)
    - Metadata JSON to stderr: {"lang": "en", "type": "manual|auto", "segment_count": 245}

Exit codes:
    0 = success
    1 = no transcript available
    2 = video not found or inaccessible / blocked
    3 = dependency missing (youtube-transcript-api not installed)
"""

import argparse
import json
import re
import sys

try:
    from youtube_transcript_api import (
        YouTubeTranscriptApi,
        NoTranscriptFound,
        TranscriptsDisabled,
        VideoUnavailable,
    )
    from youtube_transcript_api._errors import RequestBlocked, IpBlocked
except ImportError:
    print(
        "ERROR: youtube-transcript-api not installed.\n"
        "Run: bash scripts/setup.sh",
        file=sys.stderr,
    )
    sys.exit(3)


def extract_video_id(video_id_or_url: str) -> str:
    """Accept video ID or various YouTube URL formats."""
    patterns = [
        r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]
    for pattern in patterns:
        m = re.search(pattern, video_id_or_url)
        if m:
            return m.group(1)
    return video_id_or_url


def fetch_transcript(video_id: str, preferred_lang: str = "en") -> tuple[str, dict]:
    """
    Fetch transcript for a video using youtube-transcript-api v1.x.
    Returns (transcript_text, metadata_dict).
    Raises appropriate exceptions on failure.
    """
    video_id = extract_video_id(video_id)
    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.list(video_id)
    except VideoUnavailable:
        raise ValueError(f"Video {video_id} is unavailable or private")
    except TranscriptsDisabled:
        raise LookupError(f"Transcripts disabled for video {video_id}")
    except (RequestBlocked, IpBlocked) as e:
        raise ConnectionError(
            f"Request blocked by YouTube for video {video_id}. "
            "This usually means the IP is rate-limited. Try again later."
        )

    transcript = None
    transcript_meta = {"type": "auto", "lang": "en"}

    # Preference order:
    # 1. Manual in preferred lang
    # 2. Manual in English (if preferred != en)
    # 3. Generated in preferred lang
    # 4. Generated in English
    # 5. Any available transcript
    try_order = [
        (transcript_list.find_manually_created_transcript, [preferred_lang], "manual"),
    ]
    if preferred_lang != "en":
        try_order.append(
            (transcript_list.find_manually_created_transcript, ["en"], "manual")
        )
    try_order.extend([
        (transcript_list.find_generated_transcript, [preferred_lang], "auto"),
        (transcript_list.find_generated_transcript, ["en"], "auto"),
    ])

    for finder, langs, t_type in try_order:
        try:
            transcript = finder(langs)
            transcript_meta["type"] = t_type
            transcript_meta["lang"] = transcript.language_code
            break
        except NoTranscriptFound:
            continue

    if transcript is None:
        # Last resort: grab whatever is available
        available = list(transcript_list)
        if not available:
            raise LookupError(f"No transcripts available for video {video_id}")
        transcript = available[0]
        transcript_meta["type"] = "auto" if transcript.is_generated else "manual"
        transcript_meta["lang"] = transcript.language_code

    # Fetch the actual transcript data
    fetched = transcript.fetch()
    transcript_meta["segment_count"] = len(fetched)

    # Build clean text — FetchedTranscriptSnippet has .text attribute in v1.x
    lines = []
    for snippet in fetched:
        text = snippet.text.strip() if hasattr(snippet, "text") else snippet.get("text", "").strip()
        if text:
            lines.append(text)

    transcript_text = " ".join(lines)
    # Clean up common transcript artifacts
    transcript_text = re.sub(r"\s+", " ", transcript_text).strip()
    transcript_text = re.sub(r"\[.*?\]", "", transcript_text)  # Remove [Music], [Applause] etc.
    transcript_text = re.sub(r"\s+", " ", transcript_text).strip()

    return transcript_text, transcript_meta


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube transcript")
    parser.add_argument(
        "--video-id", required=True, help="YouTube video ID or URL"
    )
    parser.add_argument(
        "--lang", default="en", help="Preferred transcript language (default: en)"
    )
    parser.add_argument(
        "--output", help="Output file path (default: stdout)"
    )
    args = parser.parse_args()

    try:
        text, meta = fetch_transcript(args.video_id, args.lang)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    except LookupError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except ConnectionError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)

    # Output metadata to stderr
    print(json.dumps(meta), file=sys.stderr)

    # Output transcript
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)


if __name__ == "__main__":
    main()
