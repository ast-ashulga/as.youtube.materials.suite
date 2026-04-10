# Report Templates

These templates define the exact Markdown structure for each depth level. Use them when generating individual video reports.

---

## BRIEF (default)

Produces a compact, scannable report. Use this unless `--depth=standard` or `--depth=comprehensive` is set.

```markdown
# [Video Title]

**Channel**: [Channel Name] · **Duration**: [HH:MM:SS] · **Published**: [YYYY-MM-DD if available]
**URL**: [Full YouTube URL]

---

## Summary

[3-5 sentence overview of the video's core message and what viewers will gain. Be specific — avoid vague phrases like "this video covers many topics".]

## Key Takeaways

- [Concrete, actionable or insightful point]
- [Concrete, actionable or insightful point]
- [3-7 bullets total, each self-contained]

---

## Related in This Session

- [Related: Title of Related Video](../reports/related-video-slug.md) — [one-line reason why related]
```

---

## STANDARD

Extends Brief with quotes, actions, and terminology.

```markdown
# [Video Title]

**Channel**: [Channel Name] · **Duration**: [HH:MM:SS] · **Published**: [YYYY-MM-DD if available]
**URL**: [Full YouTube URL]

---

## Summary

[3-5 sentence overview.]

## Key Takeaways

- [Takeaway]
- [Takeaway]
- [3-7 bullets]

## Notable Quotes

> "[Exact or near-exact quote from transcript]"

> "[Another notable quote]"

## Action Items

- [ ] [Concrete action a learner/researcher could take based on this video]
- [ ] [Another action]

## Key Terminology

| Term | Definition |
|------|-----------|
| [Term] | [Concise definition as used in the video] |

---

## Related in This Session

- [Related: Title](../reports/slug.md) — [reason]
```

---

## COMPREHENSIVE

Full analysis including chapter breakdown, mental models, and speaker context.

```markdown
# [Video Title]

**Channel**: [Channel Name] · **Duration**: [HH:MM:SS] · **Published**: [YYYY-MM-DD if available]
**URL**: [Full YouTube URL]
**Speaker(s)**: [Name and brief context if identifiable]

---

## Summary

[5-8 sentence overview covering main thesis, supporting arguments, and conclusions.]

## Key Takeaways

- [Takeaway]
- [5-10 bullets]

## Chapter Breakdown

| Timestamp (approx.) | Topic | Key Points |
|---------------------|-------|-----------|
| 0:00 | Introduction | [What's covered] |
| [MM:SS] | [Topic] | [Key points] |

## Notable Quotes

> "[Quote]" — [context/timestamp if relevant]

## Mental Models & Frameworks

- **[Model Name]**: [How the video applies or explains this model]
- [2-4 models or frameworks discussed]

## Action Items

- [ ] [Action]

## Key Terminology

| Term | Definition |
|------|-----------|
| [Term] | [Definition] |

## Speaker Analysis

[2-3 sentences on the speaker's perspective, expertise signals, and potential biases.]

---

## Related in This Session

- [Related: Title](../reports/slug.md) — [reason]
```

---

## BILINGUAL SUPPLEMENT (when `--lang=en+ru`)

Append this section after all other sections in any depth level:

```markdown
---

## Резюме (Russian Summary)

**[Video Title]**

[Russian translation of the Summary section — 3-5 sentences]

### Ключевые выводы

- [Russian translation of Key Takeaways]
```
