---
name: yt-humanize
description: >-
  This skill should be used when the user wants to humanize or polish the
  reports in a research session. Use when the user says "humanize the reports",
  "make the reports sound more natural", "remove AI writing patterns",
  "polish the session output", "apply the humanizer", or "make it less AI-like".
  It applies the 29 blader humanizer patterns to all Markdown report files in
  a session. Can also be invoked automatically by yt-research with --humanize flag.
user-invocable: true
---

# yt-humanize — Report Humanizer

You remove AI writing patterns from research session reports using the blader humanizer v2.5.1 framework (29 patterns).

## Invocation Examples

```
/yt-humanize
/yt-humanize sessions/2026-04-10_claude-code/
/yt-humanize sessions/2026-04-10_claude-code/reports/specific-video.md
```

## Step 1: Find Target Files

If a session path is provided, target all `.md` files in that session:
- `{session_path}/reports/*.md`
- `{session_path}/summary.md`

If a specific file path is provided, target only that file.

If no path is provided, use the most recently modified session:
```bash
ls -t sessions/
```
Then target all reports in that session.

**Skip**: `index.md`, `sources.md`, `.session.yaml` — these are structural files, not prose.

## Step 2: Load the Patterns Reference

Read `.claude/skills/yt-humanize/references/humanizer-patterns.md`.

This contains all 29 patterns with detection rules and fix strategies. Keep this in context throughout the humanization process.

## Step 3: Humanize Each File

For each target file:

1. **Read the file** completely.
2. **Identify structure** — mark sections that are Markdown structure vs. prose:
   - DO NOT touch: headings, links, code blocks, tables (structure), blockquotes containing direct quotes, YAML frontmatter
   - DO humanize: paragraph text, bullet point text, introductory sentences
3. **Scan for patterns** — go through each of the 29 patterns and mark occurrences.
4. **Rewrite** — fix the identified issues. Changes to make:
   - Remove chatbot artifacts (#19)
   - Delete filler phrases (#22)
   - Replace AI vocabulary words (#7): delve→examine, leverage→use, utilize→use, facilitate→help/enable, underscore→shows, paramount→most important, etc.
   - Reduce excessive hedging (#23)
   - Cut generic positive conclusions (#24)
   - Fix significance inflation (#1): replace "revolutionary"/"transformative" with specific claims
   - Reduce em dash overuse (#13): max 1 per paragraph
   - Remove signposting (#27): cut "In the next section..."
   - Fix passive voice (#29): "It was found that X" → "X shows that..."
5. **Audit pass** — re-read the edited text. Ask: "Does this still sound like an AI wrote it?" If yes, revise further.
6. **Write the file** with the humanized version.

## Step 4: Preserve Critical Content

While humanizing, never:
- Change factual content (dates, names, claims from the original video)
- Remove or modify cross-reference links
- Change the Markdown heading structure
- Alter direct quotes from transcripts (in blockquotes)
- Modify anything inside code blocks

## Step 5: Report to User

```
Humanization complete

Files processed: {N}
  - {filename}: {brief description of main changes}
  - ...

Main patterns found and fixed:
  - AI vocabulary (leverage, utilize, delve): {N occurrences fixed}
  - Filler phrases: {N removed}
  - Generic conclusions: {N rewritten}
  - [other significant patterns found]
```

## Quality Check

After processing all files, re-read the first and last paragraphs of each report. If they still feel formulaic or AI-generated, do another pass on those sections specifically.

The goal: text should read like it was written by a knowledgeable person who watched these videos and is passing on what they learned — not like a system generating a structured report.
