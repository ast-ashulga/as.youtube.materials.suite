#!/usr/bin/env python3
"""
Fetch transcript for a YouTube video via Supadata.ai API.

Requires SUPADATA_API_KEY environment variable (or --api-key argument).
Get a free key at: https://supadata.ai (100 free transcripts/month).

Usage:
    python3 scripts/fetch_transcript.py --video-id WSPChlfxJyA
    python3 scripts/fetch_transcript.py --video-id WSPChlfxJyA --lang en
    python3 scripts/fetch_transcript.py --video-id WSPChlfxJyA --output /path/to/file.txt
    python3 scripts/fetch_transcript.py --video-id WSPChlfxJyA --retries 3 --delay 2.0

Output:
    - Transcript text to stdout (or --output file)
    - Metadata JSON to stderr: {"lang": "en", "type": "auto", "segment_count": 245, "method": "supadata"}

Exit codes:
    0 = success
    1 = no transcript available (transcripts disabled or video has no captions)
    2 = video not found or inaccessible after all retries
    3 = API key missing or authentication/quota error
"""

import argparse
import json
import os
import re
import sys
import time

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: bash scripts/setup.sh", file=sys.stderr)
    sys.exit(3)

SUPADATA_API_BASE = "https://api.supadata.ai/v1"


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


def clean_text(text: str) -> str:
    """Remove HTML tags, bracketed annotations, and normalize whitespace."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_transcript(
    video_id: str,
    preferred_lang: str = "en",
    max_retries: int = 3,
    base_delay: float = 2.0,
    api_key: str | None = None,
) -> tuple[str, dict]:
    """
    Fetch transcript via Supadata.ai API with retry logic.

    Returns (transcript_text, metadata_dict).
    Raises:
        PermissionError  — API key missing, invalid, or quota exceeded (no retry)
        LookupError      — no transcript available for this video (no retry)
        ConnectionError  — all retries exhausted (transient errors)
    """
    video_id = extract_video_id(video_id)

    if not api_key:
        api_key = os.environ.get("SUPADATA_API_KEY")
    if not api_key:
        raise PermissionError(
            "SUPADATA_API_KEY not set.\n"
            "Get a free key at: https://supadata.ai\n"
            "Then: export SUPADATA_API_KEY=your_key_here"
        )

    headers = {"x-api-key": api_key}
    params = {"videoId": video_id, "lang": preferred_lang}

    last_error: Exception | None = None

    for attempt in range(max_retries + 1):
        if attempt > 0:
            delay = base_delay * (2 ** (attempt - 1))
            print(
                f"[fetch_transcript] Retry {attempt}/{max_retries} after {delay:.1f}s "
                f"(video: {video_id})",
                file=sys.stderr,
            )
            time.sleep(delay)

        try:
            resp = requests.get(
                f"{SUPADATA_API_BASE}/youtube/transcript",
                headers=headers,
                params=params,
                timeout=30,
            )
        except requests.RequestException as e:
            last_error = e
            print(f"[fetch_transcript] Network error (attempt {attempt + 1}): {e}", file=sys.stderr)
            continue

        if resp.status_code == 200:
            data = resp.json()
            content = data.get("content", [])
            lang = data.get("lang", preferred_lang)
            available_langs = data.get("availableLangs", [])

            if not content:
                raise LookupError(f"Supadata returned empty transcript for video {video_id}")

            if isinstance(content, list):
                # Segment format: [{"text": "...", "offset": 0.0, "duration": 2.5, "lang": "en"}, ...]
                texts = [
                    clean_text(seg.get("text", ""))
                    for seg in content
                    if seg.get("text", "").strip()
                ]
                transcript_text = " ".join(texts)
                segment_count = len(content)
            else:
                # Plain text format
                transcript_text = clean_text(str(content))
                segment_count = transcript_text.count(". ") + transcript_text.count("? ") + 1

            if len(transcript_text.strip()) < 30:
                raise LookupError(
                    f"Transcript for video {video_id} is too short to be useful "
                    f"({len(transcript_text)} chars)"
                )

            meta = {
                "lang": lang,
                "type": "auto",
                "segment_count": segment_count,
                "method": "supadata",
                "available_langs": available_langs,
            }
            return transcript_text, meta

        elif resp.status_code == 401:
            raise PermissionError(
                "Supadata API key is invalid or expired. "
                "Check your SUPADATA_API_KEY at https://supadata.ai/dashboard"
            )

        elif resp.status_code == 402:
            raise PermissionError(
                "Supadata API quota exceeded. "
                "Upgrade your plan at https://supadata.ai/pricing or wait for the monthly reset."
            )

        elif resp.status_code == 404:
            try:
                err_msg = resp.json().get("message", resp.text[:200])
            except Exception:
                err_msg = resp.text[:200]
            raise LookupError(
                f"No transcript available for video {video_id}. "
                f"Reason: {err_msg}"
            )

        elif resp.status_code == 429:
            print(
                f"[fetch_transcript] Supadata rate limited (attempt {attempt + 1}): 429 — waiting before retry",
                file=sys.stderr,
            )
            last_error = ConnectionError("Supadata rate limit (429)")

        else:
            print(
                f"[fetch_transcript] Supadata returned {resp.status_code} "
                f"(attempt {attempt + 1}): {resp.text[:200]}",
                file=sys.stderr,
            )
            last_error = ConnectionError(f"Supadata API error {resp.status_code}")

    raise ConnectionError(
        f"All transcript fetch attempts failed for video {video_id} after {max_retries} retries. "
        f"Last error: {last_error}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Fetch YouTube transcript via Supadata.ai API"
    )
    parser.add_argument("--video-id", required=True, help="YouTube video ID or URL")
    parser.add_argument("--lang", default="en", help="Preferred transcript language (default: en)")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    parser.add_argument(
        "--retries", type=int, default=3,
        help="Max retries on rate-limited requests (default: 3)"
    )
    parser.add_argument(
        "--delay", type=float, default=2.0,
        help="Base delay in seconds between retries (default: 2.0)"
    )
    parser.add_argument("--api-key", default=None, help="Supadata API key (overrides SUPADATA_API_KEY env var)")
    # Kept for CLI compatibility — no longer functional
    parser.add_argument("--cookies-from-browser", default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.cookies_from_browser:
        print(
            "WARNING: --cookies-from-browser is no longer used. "
            "Transcript fetching now goes through Supadata.ai API.",
            file=sys.stderr,
        )

    try:
        text, meta = fetch_transcript(
            args.video_id,
            args.lang,
            args.retries,
            args.delay,
            args.api_key,
        )
    except PermissionError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)
    except LookupError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except ConnectionError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)

    # Output metadata to stderr (consumed by transcript-agent)
    print(json.dumps(meta), file=sys.stderr)

    # Output transcript text
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)


if __name__ == "__main__":
    main()
