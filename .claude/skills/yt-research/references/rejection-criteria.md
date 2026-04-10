# Video Rejection Criteria

When analyzing videos, apply these criteria to decide whether to include or reject each one. Always provide a clear rejection reason in `.session.yaml` and in `sources.md`.

---

## Automatic Rejection (No Override)

These criteria result in immediate rejection regardless of content quality:

| Criterion | Rejection Reason to Use |
|-----------|------------------------|
| No transcript available (any language) | `No transcript available` |
| Video is private or unavailable | `Video unavailable/private` |
| Duration < 2 minutes (120 seconds) | `Too short (< 2 min)` |
| Duration > 3 hours (10800 seconds) | `Too long (> 3 hours) — likely a stream or conference` |

---

## Content Relevance Rejection

Evaluate relevance after reading the transcript. Reject if:

1. **Off-topic**: Content does not address any of the session topics. Less than ~20% of the video is topically relevant.
   - Reason: `Off-topic — content unrelated to session topics`

2. **Surface-level only**: Video only mentions the topic in passing without substantive coverage.
   - Reason: `Insufficient coverage — topic mentioned but not substantively addressed`

3. **Promotional**: Video is primarily an advertisement for a product/service with minimal educational or informational value.
   - Reason: `Primarily promotional content`

---

## Duplicate/Overlap Rejection

When two videos cover the same ground:

1. **Near-duplicate**: Same speaker, same content as another video in the session (e.g., reposted or duplicated content).
   - Reason: `Duplicate of [other video title]`

2. **Significant overlap (>70% content overlap)**: Two videos cover almost identical material. Keep the one with:
   - Better transcript quality
   - More recent publication date
   - Higher relevance score
   - Reason: `Significant overlap with [other video title] — retained the more relevant video`

---

## Language Mismatch Rejection

When `--lang` is specified and a strict language match is required:

- Reject if the transcript is not in the requested language AND no translation is available.
- Reason: `Transcript language ([detected_lang]) does not match requested language ([requested_lang])`

**Note**: If a video is in another language but highly relevant, note it in `sources.md` as "potentially relevant but language mismatch" rather than silently discarding.

---

## Relevance Scoring Guide

For borderline cases, assign a relevance score (0-10) and apply this threshold:

| Score | Decision |
|-------|---------|
| 8-10 | Include — highly relevant |
| 5-7 | Include with note — moderately relevant |
| 3-4 | Borderline — include only if session has < 5 videos total |
| 0-2 | Reject — insufficient relevance |

Relevance factors:
- **Topic match** (40%): How directly does the video address the session topics?
- **Depth** (30%): Does the video go beyond surface-level treatment?
- **Uniqueness** (20%): Does this video add something not covered by other included videos?
- **Source quality** (10%): Is the speaker/channel credible and knowledgeable?

---

## Required Output in sources.md

Every candidate video (included or rejected) must appear in `sources.md` with:
- Title, channel, URL, duration
- Status: ✅ Included or ❌ Rejected
- For rejections: explicit reason
- For inclusions: 1-sentence justification of relevance
