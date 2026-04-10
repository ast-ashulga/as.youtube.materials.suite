---
name: yt-refine
description: >-
  This skill should be used when the user wants to refine, update, or extend an
  existing yt-research session. Use when the user says "add more videos on X",
  "change depth to standard", "remove this video", "re-analyze with focus on Y",
  "add these URLs to the session", "update my research", or "refine the session".
  It reads the existing session state, computes the delta, and re-processes only
  what changed — preserving already-fetched transcripts.
user-invocable: true
---

# yt-refine — Iterative Session Refinement

You refine an existing research session based on new instructions without reprocessing unchanged work.

## Invocation Examples

```
/yt-refine "add MCP servers as a topic"
/yt-refine "change depth to standard"
/yt-refine --url https://www.youtube.com/watch?v=NEW_ID
/yt-refine "remove the video about basics, it's off-topic"
/yt-refine "focus analysis on practical examples, not theory"
```

## Step 1: Find the Session

List available sessions:
```bash
ls -t sessions/
```

If the user specified a session ID, use that. Otherwise, use the most recently modified session directory (first result from `ls -t`).

Read `{session_path}/.session.yaml` to load current state.

Confirm with user (just a brief message, no blocking wait):
"Refining session `{session_id}` — currently {N} included videos, depth: {depth}."

## Step 2: Parse Refinement Instructions

From the user's message, extract what changed:

| Change Type | Detection | Action |
|------------|-----------|--------|
| New topics added | "add topic", new topic phrases | Search + transcript + analysis for new videos |
| New URLs added | YouTube URLs in message | Transcript + analysis for new URLs |
| Topics removed | "remove topic X", "stop researching X" | Mark related videos as removed, re-consolidate |
| Specific video removed | "remove [title]", "drop [title]" | Mark as `status: removed`, re-consolidate |
| Depth changed | "change depth to", "--depth=X" | Re-analyze ALL existing transcripts (no re-fetch), re-consolidate |
| Instructions changed | "focus on X", "re-analyze with Y" | Re-analyze ALL existing transcripts, re-consolidate |
| Humanize | "--humanize" | Run humanizer on all reports |
| Language change | "--lang=X" | Re-analyze all, re-consolidate |

## Step 3: Execute the Delta

### For new topics/URLs:
- Run search agent for new topics only
- Run transcript agents for new videos only
- Run analysis agents for new videos only
- Then re-consolidate (all videos)

### For depth/instruction changes (no new videos):
- Skip search and transcript steps entirely (transcripts already in `transcripts/`)
- Run analysis agents for ALL videos that have transcripts (not just new ones)
- Re-consolidate

### For video removal only:
- Update `.session.yaml`: set `status: removed` for matching video(s)
- Skip search, transcript, and analysis
- Re-consolidate only

### For humanize only:
- Skip all research steps
- Run humanizer on existing reports

**Key optimization**: Never re-fetch transcripts that already exist in `transcripts/` with non-zero size. Always check before spawning a transcript agent.

## Step 4: Update .session.yaml

Append to the history array:
```yaml
- timestamp: "{ISO datetime}"
  action: "refined"
  details: "{summary of what changed}"
  changes:
    topics_added: []
    topics_removed: []
    urls_added: []
    videos_removed: []
    depth_changed: null  # or "brief -> standard"
    instructions_changed: "{new instructions if any}"
```

Update the config section with new values.

## Step 5: Report to User

```
Refinement complete for session {session_id}

Changes applied:
  {bullet list of what was changed}

Updated results:
  Included: {N} videos (+{delta})
  Rejected: {M} videos
  
Files updated in sessions/{session_id}/
```

## Conflict Resolution

- If a video was previously rejected but is now being explicitly added by URL: override the rejection and include it.
- If a depth change would cause fewer fields (e.g., comprehensive → brief): keep the extra fields in the report (they're not wrong, just extra).
- If both old and new analyses exist for a video (due to instruction changes): use the new analysis.

## Preserving Work

Deleted videos' transcripts and analysis results are **not deleted from disk** — only their status changes in `.session.yaml`. This allows undoing a removal in a subsequent refinement.
