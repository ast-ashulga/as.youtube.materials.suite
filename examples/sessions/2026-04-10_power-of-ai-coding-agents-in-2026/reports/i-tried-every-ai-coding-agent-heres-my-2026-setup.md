# I Tried Every AI Coding Agent... Here's My 2026 Setup

**Channel**: Your Average Tech Bro · **Duration**: 20:25 · **Published**: 2026-01-28
**URL**: https://www.youtube.com/watch?v=zgxorh9LhiE

---

## Summary

A solo developer building a startup (Yorby) describes his complete AI coding workflow as of January 2026. He uses Claude Code with Opus 4.5 on the $200/month Max plan as his primary coding engine, GPT 5.2 Codex for large slow refactors, and Gemini 3 Pro for UI/UX generation. The key workflow practice is Git worktrees — managed via the Branchlet CLI — to run multiple parallel AI coding agents on isolated branches simultaneously without merge conflicts. He also keeps per-feature claude.md context files that auto-update on every PR via a custom skill, which he calls the single biggest unlock for AI accuracy in a growing codebase.

## Key Takeaways

- Claude Code + Opus 4.5 is the primary agentic workhorse: the $200/month Max plan provides 20x usage to avoid rate limits
- Different models serve different roles: GPT 5.2 Codex for large slow refactors; Gemini 3 Pro for UI/UX; Composer 1 for quick iterative changes
- Always use Plan Mode before executing: ask the AI to show its plan first before taking any action
- Parallel agents via Git worktrees (managed with Branchlet CLI) enable concurrent development without merge conflicts
- Per-feature claude.md files auto-updated on every PR are the single biggest unlock for AI accuracy in large codebases
- Avoid one-shotting complex features in large codebases — build step-by-step instead
- No-code tools like MindStudio are legitimate velocity tools for recurring data workflows

## Notable Quotes

> "I almost always default to using any plan mode first just to make sure it has sufficient time to gather the context."

> "Creating these claude.md files and making sure they get updated with every single code change has significantly decreased the amount of manual files I have to tag within Claude."

> "True velocity is just using whatever is the best and fastest solution out there and not reinventing the wheel."

## Action Items

- [ ] Set up per-feature claude.md files and create a Claude Code skill that auto-updates them on every PR
- [ ] Install Branchlet CLI and configure Git worktrees for parallel AI agent sessions
- [ ] Audit model usage by task type: Claude Opus 4.5 for general agentic work, GPT 5.2 Codex for large refactors, Gemini 3 Pro for UI
- [ ] Enforce Plan Mode: require AI to present its plan before executing any task
- [ ] Build a design system doc by collecting admired UI screenshots and feeding them to Gemini 3 Pro

## Key Terminology

| Term | Definition |
|------|-----------|
| Plan Mode | Mode where AI presents its intended approach before executing — improves quality and provides a review checkpoint |
| Git Worktree | Separate working directories tied to different branches, used to run parallel AI agents without conflicts |
| Branchlet | Open-source CLI for managing Git worktrees for parallel agent sessions |
| claude.md | Per-feature context file auto-updated on every PR, dramatically improving AI accuracy in large codebases |
| One-shotting | Asking AI to build an entire feature in a single prompt — degrades quality in large codebases |

---

## Related in This Session

- [Related: The Only AI Coding Tools Worth Learning in 2026](../reports/the-only-ai-coding-tools-worth-learning-in-2026.md) — same Claude Code focus; complementary tool landscape perspective
- [Related: Best AI Coding Tools for Developers in 2026](../reports/best-ai-coding-tools-for-developers-in-2026.md) — both emphasize project context files (CLAUDE.md) and plan-before-execute workflow
- [Related: What is Agentic AI Engineering (Meta Staff Engineer Explains)](../reports/what-is-agentic-ai-engineering-meta-staff-engineer.md) — both cover parallel agents, context engineering, and codebase optimization for AI
- [Related: How I'm Using AI Agents in 2026](../reports/how-im-using-ai-agents-in-2026.md) — both demonstrate running multiple parallel agents simultaneously

---

## Резюме (Russian Summary)

**I Tried Every AI Coding Agent... Here's My 2026 Setup**

Разработчик-одиночка, строящий стартап Yorby, описывает рабочий процесс с ИИ-инструментами по состоянию на январь 2026 года. Основной инструмент — Claude Code с Opus 4.5 (тариф Max, $200/мес.). Ключевое нововведение — параллельные ИИ-агенты через Git worktrees с помощью CLI-утилиты Branchlet. Сеть claude.md-файлов (по одному на каждую фичу), автоматически обновляемых при каждом PR, обеспечивает точность AI-ответов в растущей кодовой базе.

### Ключевые выводы

- Claude Code + Opus 4.5 — основной инструмент: тариф Max ($200/мес.) даёт 20x использования
- Разные модели — для разных задач: Codex для рефакторинга, Gemini 3 Pro для UI
- Режим планирования обязателен перед выполнением любой задачи
- Параллельные агенты через Git worktrees (Branchlet) без конфликтов слияния
- Файлы claude.md на каждую фичу + автообновление при PR — главный разблокировщик контекста
