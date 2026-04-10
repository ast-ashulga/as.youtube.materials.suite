---
name: yt-research
description: >-
  This skill should be used when the user asks to "research YouTube videos on a
  topic", "find and summarize YouTube content", "create learning materials from
  YouTube", "generate a research session from YouTube", "analyze YouTube videos",
  "make a report from YouTube videos", or provides YouTube URLs for analysis. It
  orchestrates video discovery, transcript extraction, analysis, and consolidated
  wiki-style report generation. Also use when the user says things like "research
  [topic] on YouTube", "summarize these YouTube links", or "build a knowledge
  base from these videos".
user-invocable: true
---

# yt-research — YouTube Research Orchestrator

You are a YouTube research orchestrator. When invoked, you run a fully automated end-to-end pipeline to produce consolidated, wiki-style research materials from YouTube videos.

## Invocation Examples

```
/yt-research "Claude Code" "MCP servers"
/yt-research "machine learning basics" --depth=standard --max-videos=10
/yt-research --url https://www.youtube.com/watch?v=ID "additional topic"
/yt-research "AI agents" --humanize --lang=en+ru
```

## Parsing User Input

From the user's message, extract:
- **topics**: quoted strings or topic phrases (e.g., "Claude Code", "MCP servers")
- **urls**: any YouTube URLs provided directly
- **--depth**: `brief` (default) | `standard` | `comprehensive`
- **--humanize**: flag to apply humanizer to all reports (default: false)
- **--lang**: `en` (default) | `ru` | `en+ru`
- **--max-videos**: integer (default: 12)
- **--min-duration**: seconds (default: 120)
- **--max-duration**: seconds (default: 10800)
- **additional instructions**: any natural language instructions about focus, format, or content preferences

If no topics and no URLs are provided, ask the user: "What topics or YouTube URLs should I research?"

## Step 1: Environment Setup

Determine the project root (the directory containing `scripts/` and `.claude/`). This should be the working directory when the skill is invoked.

Check if venv exists:
```bash
test -f .venv/bin/python && echo "ok" || echo "missing"
```

If venv is missing or the check fails, run:
```bash
bash scripts/setup.sh
```

## Step 2: Create Session Directory

Generate session ID from current date and first topic:
```
session_id = YYYY-MM-DD_{slugified-first-topic}
session_path = ./sessions/{session_id}/
```

If a session with this ID already exists, append `-2`, `-3`, etc.

Create directory structure:
```bash
mkdir -p {session_path}/transcripts
mkdir -p {session_path}/reports
```

Write initial `.session.yaml`:
```yaml
session_id: "{session_id}"
created: "{ISO datetime}"
updated: "{ISO datetime}"
config:
  topics: {topics list}
  urls: {urls list}
  depth: "{depth}"
  humanize: {humanize bool}
  lang: "{lang}"
  max_videos: {max_videos}
  min_duration: {min_duration}
  max_duration: {max_duration}
  additional_instructions: "{any extra instructions}"
candidates: []
videos: []
history:
  - timestamp: "{ISO datetime}"
    action: "created"
    details: "Session started with {N} topics and {M} direct URLs"
```

Tell the user: "Starting research session `{session_id}`. I'll search for videos, fetch transcripts, and generate reports."

## Step 3: Discover Videos

### 3a. User-provided URLs
For each URL provided directly by the user, add to candidates immediately:
```yaml
- url: "{url}"
  id: "{extracted video id}"
  title: "pending"
  channel: "pending"
  duration: 0
  source: "user-provided"
```

### 3b. Topic-based search (if topics provided)
If there are topics, spawn a search agent to find videos.

Read the search agent prompt from `.claude/skills/yt-research/agents/search-agent.md`.

Spawn an Agent with that prompt, providing:
- topics, max_videos, lang, min_duration, max_duration, session_path
- project_root (absolute path to project directory)

Wait for the agent to complete and return its result JSON.

After the search agent completes, read the updated `.session.yaml` to get the full candidate list.

Tell the user: "Found {N} candidate videos. Starting transcript fetch..."

## Step 4: Fetch Transcripts (Parallel)

Read the transcript agent prompt from `.claude/skills/yt-research/agents/transcript-agent.md`.

Spawn transcript agents in parallel batches of up to 3. For each candidate video:
- Pass: video_url, video_id, video_slug, session_path, lang, project_root

After each batch of transcript agents completes, wait 3-5 seconds before spawning the next batch. This spacing reduces the chance of YouTube rate-limiting when processing many videos at once.

Collect all results. Update `.session.yaml` with transcript status for each video.

Track counts:
- `fetched`: videos where transcript was successfully retrieved
- `rejected_transcript`: videos rejected due to no transcript

Tell the user: "Transcripts fetched: {fetched}/{total}. Starting analysis..."

## Step 5: Analyze Transcripts (Parallel)

Read the analysis agent prompt from `.claude/skills/yt-research/agents/analysis-agent.md`.

For each video with `status: "transcript_fetched"`, spawn an analysis agent in parallel batches of 5.

Pass to each agent:
- transcript_file, metadata_file, session_topics, depth, session_path, project_root
- Report templates path: `.claude/skills/yt-research/references/report-templates.md`
- Rejection criteria path: `.claude/skills/yt-research/references/rejection-criteria.md`

Collect all analysis results. Update `.session.yaml` with analyzed status for each video.

Track:
- `included`: analyses where `relevant: true`
- `rejected_content`: analyses where `relevant: false`

Tell the user: "{included} videos included, {rejected} rejected as irrelevant. Generating reports..."

## Step 6: Generate Consolidated Output

Read the consolidation agent prompt from `.claude/skills/yt-research/agents/consolidation-agent.md`.

Spawn a single consolidation agent with:
- All analysis results (both included and rejected)
- session_config (from .session.yaml)
- session_path
- report_templates_path: `.claude/skills/yt-research/references/report-templates.md`
- cross_reference_guide_path: `.claude/skills/yt-research/references/cross-reference-guide.md`

Wait for consolidation to complete.

## Step 7: Humanize (if --humanize flag)

If `--humanize` was requested, invoke the yt-humanize skill on this session:

Spawn an Agent using the yt-humanize skill logic (read `.claude/skills/yt-humanize/SKILL.md`), passing the session_path.

## Step 8: Final Report to User

Tell the user:

```
Research session complete: {session_id}

Results:
  Included: {N} videos
  Rejected: {M} videos  
  Session folder: sessions/{session_id}/

Files generated:
  sessions/{session_id}/index.md       — Start here
  sessions/{session_id}/summary.md     — Consolidated findings
  sessions/{session_id}/sources.md     — All sources with status
  sessions/{session_id}/reports/       — {N} individual video reports

To refine this session:
  /yt-refine "add more videos on X" or "change depth to standard"
```

## Error Handling

- If setup.sh fails, stop and show the error to the user.
- If search finds 0 candidates AND no URLs provided, ask the user to provide URLs or refine the topics.
- If all transcripts fail (likely IP rate-limiting despite automatic retries), inform the user: "YouTube is rate-limiting transcript requests from this IP. Try: (1) wait a few minutes and retry with /yt-refine, or (2) add --cookies-from-browser chrome to your next /yt-research call to authenticate via your browser session."
- If an individual step fails, log it but continue processing other videos.
- Always produce output even if some videos failed — partial results are better than none.

## Additional Instructions

If the user provided additional instructions (e.g., "focus on practical examples", "ignore theoretical content", "I'm a beginner"), pass these to the analysis agents as context for relevance scoring and content extraction.
