# as.youtube.materials.suite

Agentic suite for Claude Code that processes YouTube videos into consolidated, wiki-style learning and research materials.

## What It Does

Provide topics (and optionally specific YouTube URLs). The suite:
1. Discovers relevant YouTube videos via search
2. Fetches their transcripts
3. Analyzes each one for relevance and extracts insights
4. Generates a folder of linked Markdown files: summary, individual video reports, and a sources list with rejection explanations

## Setup

### 1. Install dependencies

```bash
bash scripts/setup.sh
```

Requires Python 3.11+.

### 2. Get API keys (both free)

**YouTube Data API v3** — for video search and metadata (10,000 units/day free)

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com)
2. Enable the YouTube Data API v3
3. Create an API key under **Credentials**

**Supadata.ai** — for transcript fetching (100 transcripts/month free)

1. Sign up at [supadata.ai](https://supadata.ai)
2. Copy your API key from the dashboard

### 3. Export the keys

```bash
export YOUTUBE_API_KEY=your_youtube_key_here
export SUPADATA_API_KEY=your_supadata_key_here
```

Add both lines to `~/.zshrc` (or `~/.bashrc`) so they persist across sessions.

## Usage

In Claude Code, use the slash commands:

### Start a research session
```
/yt-research "Claude Code" "MCP servers"
/yt-research "machine learning basics" --depth=standard --max-videos=10
/yt-research --url https://www.youtube.com/watch?v=ID "additional topic"
/yt-research "AI agents" --humanize --lang=en+ru
```

### Refine an existing session
```
/yt-refine "add more videos on tool use"
/yt-refine "change depth to standard"
/yt-refine --url https://www.youtube.com/watch?v=NEW_ID
/yt-refine "focus analysis on practical examples"
```

### Polish reports
```
/yt-humanize
```

## Output

Each session creates a folder: `sessions/YYYY-MM-DD_topic-slug/`

| File | Contents |
|------|---------|
| `index.md` | Landing page — navigation hub for the session |
| `summary.md` | Consolidated findings, key insights, recommended reading order |
| `sources.md` | All candidate videos with included/rejected status and reasons |
| `reports/*.md` | Individual video report pages with cross-references |

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--depth` | `brief`, `standard`, `comprehensive` | `brief` | Report detail level |
| `--max-videos` | integer | 12 | Max videos to include |
| `--humanize` | flag | off | Remove AI writing patterns from reports |
| `--lang` | `en`, `ru`, `en+ru` | `en` | Output language |
| `--min-duration` | seconds | 120 | Filter out very short videos |
| `--max-duration` | seconds | 10800 | Filter out very long videos |

## Depth Levels

- **brief** (default): Summary + Key Takeaways
- **standard**: + Notable Quotes, Action Items, Key Terminology
- **comprehensive**: + Chapter Breakdown, Mental Models, Speaker Analysis

## Example Session

See [`examples/sessions/2026-04-10_power-of-ai-coding-agents-in-2026/`](examples/sessions/2026-04-10_power-of-ai-coding-agents-in-2026/) for a complete example output.

- **Topic**: Power of AI Coding Agents in 2026
- **Depth**: standard
- **Videos**: 20 included across 5 themes (Agent Fundamentals, Developer Workflow, Tool Landscape, No-Code Platforms, Trends)
- **Languages**: English + Russian

Start from [`index.md`](examples/sessions/2026-04-10_power-of-ai-coding-agents-in-2026/index.md) to navigate the session.
