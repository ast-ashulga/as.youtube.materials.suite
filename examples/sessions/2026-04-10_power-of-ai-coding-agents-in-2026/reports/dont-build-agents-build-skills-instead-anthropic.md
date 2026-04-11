# Don't Build Agents, Build Skills Instead – Barry Zhang & Mahesh Murag, Anthropic

**Channel**: AI Engineer · **Duration**: 16:22 · **Published**: 2025-12-08
**URL**: https://www.youtube.com/watch?v=CEvIs9y1uog

---

## Summary

Anthropic engineers Barry Zhang and Mahesh Murag argue that agents like Claude Code are already general-purpose — effectively a universal interface to the digital world through code — but lack domain expertise. Their solution is "Skills": organized folders of markdown files, scripts, and assets that package procedural knowledge in a format agents can dynamically load at runtime. Skills are simple enough for non-technical users to build, can be versioned in Git, and work together in combination. MCP (Model Context Protocol) and Skills serve different purposes: MCP handles external connectivity while Skills carry internal domain expertise. The long-term goal is a self-improving knowledge base where agents create and refine Skills over time using a meta "Skill Creator Skill."

## Key Takeaways

- Agents are general-purpose — Claude Code is essentially a universal agent using code as an interface to the digital world; building separate agents per domain is no longer necessary
- The missing piece is domain expertise, not intelligence — like choosing an experienced tax professional over a mathematical genius
- Skills are simply folders — markdown files, scripts, and assets packaging domain know-how; simple enough for non-technical users to build and maintain
- Progressive disclosure protects the context window — only skill metadata is shown at all times; full content is read on-demand
- MCP and Skills complement each other — MCP for external connectivity, Skills for internal domain expertise
- Non-technical users in finance, legal, and recruiting are already building Skills successfully
- Skills enable continuous learning — the standardized file-based format makes knowledge transferable to future agent versions

## Notable Quotes

> "Who do you want doing your taxes? An experienced tax professional or a mathematical genius? I'd pick Barry every time." — Barry Zhang

> "Code is not just a use case but the universal interface to the digital world." — Barry Zhang

> "A skill built by someone else in the community will help make your own agents more capable." — Mahesh Murag

> "Our goal is that Claude on day 30 is going to be a lot better than Claude on day one." — Mahesh Murag

## Action Items

- [ ] Audit current agent implementations — evaluate if a single general agent with Skills can replace domain-specific agents
- [ ] Start packaging domain know-how as Skills: create SKILL.md with instructions, add reusable scripts as tools, and version in Git
- [ ] Map MCP servers to Skills: MCP for external data access, Skills for procedural knowledge
- [ ] Enable non-technical team members to build Skills for their domains
- [ ] Plan for skill versioning and evaluation as they grow more complex

## Key Terminology

| Term | Definition |
|------|-----------|
| Skills | Organized folders of markdown files and scripts packaging composable procedural knowledge, dynamically loaded at runtime |
| Progressive Disclosure | Mechanism showing only skill metadata at all times; full content is read on-demand to protect context window |
| MCP (Model Context Protocol) | Standard for agent connectivity to external tools; provides outside-world connection while Skills provide domain expertise |
| Composability | Combining multiple independent Skills so a single general agent can handle diverse tasks |
| Skill Creator Skill | Meta-skill that Claude uses to create new Skills autonomously, enabling continuous self-improvement |

---

## Related in This Session

- [Related: Best AI Coding Tools for Developers in 2026](../reports/best-ai-coding-tools-for-developers-in-2026.md) — Skills are the Anthropic implementation of "agent skills" referenced as a Claude Code capability
- [Related: What is Agentic AI Engineering (Meta Staff Engineer Explains)](../reports/what-is-agentic-ai-engineering-meta-staff-engineer.md) — Skills are the knowledge store that agentic engineering encodes as the "second brain"
- [Related: 2026: The Year The IDE Died — Steve Yegge & Gene Kim](../reports/2026-the-year-the-ide-died-steve-yegge-gene-kim-vibe-coding.md) — contrasting architecture view; Skills address the domain expertise gap Yegge identifies in general agents
- [Related: AI Agents, Clearly Explained](../reports/ai-agents-clearly-explained.md) — foundational framework; Skills are the mechanism through which general agents acquire domain decision-making capability

---

## Резюме (Russian Summary)

**Don't Build Agents, Build Skills Instead – Barry Zhang & Mahesh Murag, Anthropic**

Инженеры Anthropic объясняют, что агентам нужны не интеллект, а доменные знания. Решение — «навыки»: структурированные папки с markdown-файлами, загружаемые динамически. MCP + Навыки дополняют друг друга. Цель: самосовершенствующаяся база знаний, в которой агенты сами создают навыки.

### Ключевые выводы

- Агенты стали универсальными — строить отдельный агент для каждой области больше не нужно
- Недостающее звено — доменная экспертиза, не интеллект
- Навык — просто папка: markdown-файлы и скрипты, доступные даже нетехническим пользователям
- Прогрессивное раскрытие защищает контекстное окно
- MCP — для внешней связности, навыки — для внутренней экспертизы; вместе покрывают любую вертикаль
