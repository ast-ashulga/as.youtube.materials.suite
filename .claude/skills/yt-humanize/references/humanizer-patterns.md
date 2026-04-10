# Humanizer Patterns Reference

Based on blader/humanizer v2.5.1 — 29 identified AI writing patterns.

When humanizing text, scan for each pattern below and rewrite affected sections. Preserve all Markdown structure (headings, links, lists, code blocks). Only rewrite prose.

---

## Content Patterns

### 1. Significance Inflation
**Detect**: Words like "groundbreaking", "revolutionary", "transformative", "unprecedented", "paradigm-shifting", "crucial", "vital", "essential" when not backed by evidence.
**Fix**: Replace with specific, measurable claims or remove the qualifier.
- Before: "This revolutionary approach fundamentally transforms how we think about AI."
- After: "This approach changes how we build AI — specifically by removing the need for labeled data."

### 2. Notability Name-Dropping
**Detect**: Invoking authority figures to add weight without engaging their ideas: "As Einstein said...", "According to leading experts..."
**Fix**: Either drop the name or engage the idea directly.

### 3. Superficial -ing Analyses
**Detect**: Sentences starting with present-participle phrases that don't add meaning: "Building on this foundation...", "Recognizing the importance of...", "Understanding that..."
**Fix**: Cut the opener and start with the actual claim.
- Before: "Building on this foundation, we can see that..."
- After: "The result is..."

### 4. Promotional Language
**Detect**: Sales-pitch phrasing: "state-of-the-art", "best-in-class", "industry-leading", "cutting-edge", "powerful solution"
**Fix**: Describe specifically what makes it notable, or remove.

### 5. Vague Attributions
**Detect**: "Studies show...", "Research indicates...", "Experts agree...", "Many people believe..." without specifics.
**Fix**: Name the study, or remove if unverifiable.

### 6. Formulaic "Challenges" Sections
**Detect**: A paragraph or section that lists challenges without analysis, often as the third item in a three-part structure (Background → Solution → Challenges).
**Fix**: Integrate challenges into the main discussion or drop if superficial.

---

## Language Patterns

### 7. AI Vocabulary Words
**Detect**: These specific words are statistically overrepresented in AI writing: *delve, tapestry, landscape, nuanced, multifaceted, comprehensive, robust, leverage, utilize, facilitate, paramount, intricate, pivotal, underscore, holistic, synergy, foster, navigating, embark*
**Fix**: Replace with simpler, more direct alternatives or cut entirely.
- "delve into" → "look at", "examine", or nothing
- "leverage" → "use"
- "facilitate" → "help", "enable", or restructure the sentence
- "underscore" → "shows", "confirms"
- "paramount" → "most important" or cut

### 8. Copula Avoidance
**Detect**: Tortured constructions to avoid "is/are": "The approach sees [X] becoming..." instead of "[X] is becoming..."
**Fix**: Use "is/are" directly.

### 9. Negative Parallelisms
**Detect**: "not only X but also Y" structures used excessively, or paired with sycophantic framing.
**Fix**: Pick the more important point and state it directly.

### 10. Rule of Three Overuse
**Detect**: Lists of exactly three items in every paragraph, especially when the third feels forced: "It improves speed, accuracy, and overall user experience."
**Fix**: Vary list lengths. Two items or four are fine.

### 11. Synonym Cycling
**Detect**: Using multiple synonyms for the same concept in close proximity to appear sophisticated: "the methodology, approach, and framework..."
**Fix**: Pick one term and use it consistently.

### 12. False Ranges
**Detect**: Vague numerical ranges that add no precision: "dozens of", "hundreds of", "a wide variety of"
**Fix**: Use actual numbers or "many" if specifics are unknown.

---

## Style Patterns

### 13. Em Dash Overuse
**Detect**: Em dashes used more than once per paragraph, or used where a comma or period works fine.
**Fix**: Replace most with commas, periods, or parentheses.

### 14. Boldface Overuse
**Detect**: More than 3-4 bolded terms per section, or bolding entire phrases rather than key terms.
**Fix**: Reserve bold for genuinely critical terms only.

### 15. Inline-Header Lists
**Detect**: Lists where each item starts with a bolded "label:" — **Speed:** Fast processing. **Accuracy:** High precision.
**Fix**: Either use a proper table or write in prose.

### 16. Title Case Headings
**Detect**: Section headings in Title Case where Sentence case is more natural in context.
**Fix**: Use sentence case unless the style guide specifies otherwise.

### 17. Emojis in Professional Writing
**Detect**: Emojis in headers, bullet points, or inline text in research/analytical content.
**Fix**: Remove emojis from professional/research content. Keep only if user-specified.

### 18. Curly Quotation Marks for Code
**Detect**: Using "smart quotes" around code, commands, or technical terms instead of `backticks`.
**Fix**: Use backticks for code, straight quotes for quotations.

---

## Communication Patterns

### 19. Chatbot Artifacts
**Detect**: "Great question!", "Certainly!", "Of course!", "I'd be happy to...", "As an AI...", "I hope this helps!"
**Fix**: Delete entirely. Start with the actual content.

### 20. Knowledge-Cutoff Disclaimers
**Detect**: Unnecessary temporal hedging: "As of my last update...", "At the time of writing...", "This information may be outdated..."
**Fix**: Remove if the information is presented as current. Add a specific date if currency matters.

### 21. Sycophantic Tone
**Detect**: Excessive praise of the subject, framing everything positively, avoiding criticism.
**Fix**: Add honest assessment. Note trade-offs, limitations, or criticisms where warranted.

---

## Filler and Hedging

### 22. Filler Phrases
**Detect**: Phrases that add length without meaning:
- "It is worth noting that..."
- "It is important to understand that..."
- "In this context..."
- "As we can see..."
- "When all is said and done..."
- "At the end of the day..."
- "In conclusion, it is clear that..."
**Fix**: Delete the filler and start with the actual content.

### 23. Excessive Hedging
**Detect**: Every claim qualified: "may potentially", "could possibly", "it seems that perhaps", "one might argue"
**Fix**: State claims directly. Add hedging only where genuine uncertainty exists.

### 24. Generic Positive Conclusions
**Detect**: Paragraphs or sections that end with a vague positive statement: "This opens up exciting new possibilities.", "The future is bright for this technology.", "This represents a significant step forward."
**Fix**: End with the specific finding or cut the conclusion entirely.

---

## Extended Patterns (v2.5.1 additions)

### 25. Hyphenated Word Pair Overuse
**Detect**: Excessive hyphenated compound modifiers: "user-friendly", "data-driven", "cutting-edge", "forward-thinking", "best-in-class" used repeatedly.
**Fix**: Use the simpler word or rephrase.

### 26. Persuasive Authority Tropes
**Detect**: Framing as consensus when it isn't: "It is widely accepted that...", "Experts universally agree...", "There is no doubt that..."
**Fix**: Name specific sources or soften to "some researchers argue".

### 27. Signposting and Announcements
**Detect**: Announcing what you're about to say before saying it: "In the next section, I will explain...", "What follows is an overview of...", "This section covers..."
**Fix**: Cut the announcement, start with the content.

### 28. Fragmented Headers
**Detect**: Single-word or two-word section headers with no context: "Overview", "Background", "Analysis", "Conclusion" — all in a row.
**Fix**: Make headers informative: "What Makes This Approach Different", "Three Limitations Worth Knowing".

### 29. Passive Voice and Subjectless Fragments
**Detect**: "It was found that...", "It can be seen that...", "It has been noted...", "It is believed..."
**Fix**: Identify who found/saw/noted it and use active voice: "[Researcher] found that...", "The data shows..."

---

## Application Process

1. Read the full text once before making any changes.
2. For each of the 29 patterns: scan text, note locations.
3. Rewrite in passes — don't try to fix all patterns in one pass.
4. After rewriting, do a final check: does it sound like a knowledgeable human wrote this, or still like an AI?
5. Preserve all Markdown structure (headings, bold, code, links) — only modify prose content.
6. Do not change factual content, source references, or cross-links.
