# YouTube Materials Suite

An agentic suite for Claude Code that processes YouTube videos into consolidated, wiki-style research materials.

## Skills (Slash Commands)

| Command | Purpose |
|---------|---------|
| `/yt-research` | Start a new research session from topics and/or URLs |
| `/yt-refine` | Refine an existing session (add topics, change depth, etc.) |
| `/yt-humanize` | Apply the AI writing pattern remover to session reports |

### /yt-research usage
```
/yt-research "topic1" "topic2"
/yt-research "topic" --depth=standard --max-videos=10
/yt-research --url https://www.youtube.com/watch?v=ID "extra topic"
/yt-research "topic" --humanize --lang=en+ru
```

### /yt-refine usage
```
/yt-refine "add more videos on X"
/yt-refine --url https://www.youtube.com/watch?v=NEW_ID
/yt-refine "change depth to standard"
/yt-refine "focus on practical examples"
```

## Project Structure

```
.claude/
  settings.json               # Hooks and auto-permissions
  skills/
    yt-research/
      SKILL.md                # Main orchestrator
      agents/
        search-agent.md       # Video discovery sub-agent prompt
        transcript-agent.md   # Transcript fetching sub-agent prompt
        analysis-agent.md     # Per-video analysis sub-agent prompt
        consolidation-agent.md # Final synthesis sub-agent prompt
      references/
        report-templates.md   # Brief/Standard/Comprehensive templates
        rejection-criteria.md # Video filtering rules
        cross-reference-guide.md # Link syntax and index/summary structure
    yt-refine/SKILL.md        # Iterative refinement skill
    yt-humanize/
      SKILL.md                # Humanizer skill
      references/
        humanizer-patterns.md # 29 AI writing patterns (blader v2.5.1)
scripts/
  setup.sh                    # One-time: create venv, install deps
  requirements.txt            # youtube-transcript-api
  search_youtube.py           # yt-dlp search wrapper
  fetch_transcript.py         # youtube-transcript-api wrapper
  extract_metadata.py         # yt-dlp metadata extractor
sessions/                     # Output (gitignored) — one folder per session
```

## Environment Requirements

- **Python 3.11+** — for scripts
- **yt-dlp** — system-installed (brew install yt-dlp). Used for video search and metadata.
- **youtube-transcript-api** — installed in `.venv/`. Used for transcript fetching.
- **Virtual environment** — at `.venv/`. Run `bash scripts/setup.sh` to create it.

### Quick setup
```bash
bash scripts/setup.sh
```

### Manual script usage
```bash
source .venv/bin/activate

# Search YouTube
python3 scripts/search_youtube.py --query "Claude Code" --max-results 5

# Fetch transcript
python3 scripts/fetch_transcript.py --video-id WSPChlfxJyA --lang en

# Get video metadata
python3 scripts/extract_metadata.py --url "https://www.youtube.com/watch?v=WSPChlfxJyA"
```

## Session Output Structure

```
sessions/YYYY-MM-DD_topic-slug/
  .session.yaml     # State: config, candidates, per-video status, history
  index.md          # Landing page — start here
  summary.md        # Consolidated findings across all videos
  sources.md        # All candidates: included + rejected with reasons
  transcripts/      # Raw transcripts (intermediate, not for user reading)
  reports/          # Individual video report pages
    video-slug.md
    ...
```

## Report Depth Levels

| Level | Contents |
|-------|---------|
| `brief` (default) | Summary, Key Takeaways, cross-references |
| `standard` | + Notable Quotes, Action Items, Key Terminology |
| `comprehensive` | + Chapter Breakdown, Mental Models, Speaker Analysis |

## Sub-Agent Guidelines

When spawning sub-agents from yt-research:
- Always pass `session_path` as an absolute path
- Transcript agents should be spawned in parallel (batches of 5)
- Analysis agents should be spawned in parallel (batches of 5)
- The consolidation agent runs last, after all analyses
- Sub-agents communicate via file system: transcripts written to `transcripts/`, state tracked in `.session.yaml`

## Script Error Codes

| Script | Exit 0 | Exit 1 | Exit 2 | Exit 3 |
|--------|--------|--------|--------|--------|
| search_youtube.py | Found videos | No results | yt-dlp error | — |
| fetch_transcript.py | Success | No transcript | Video unavailable/blocked | Dep missing |
| extract_metadata.py | Success | Video not found | yt-dlp error | — |

## Known Limitations

- **Transcript API rate limiting**: YouTube may block transcript requests if many are made in quick succession from the same IP. If this happens, the affected videos are marked as rejected with reason "Request blocked". Wait a few minutes and retry with `/yt-refine`.
- **yt-dlp metadata**: Direct URL metadata fetch may be blocked by YouTube bot detection. The script falls back to the search extractor automatically.
- **Auto-generated transcripts**: Many videos only have auto-generated transcripts, which can have word-salad sections. Analysis agents are instructed to handle this gracefully.
