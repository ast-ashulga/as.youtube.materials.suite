# AI Agents, Clearly Explained

**Channel**: Jeff Su · **Duration**: 10:09 · **Published**: 2025-04-08
**URL**: https://www.youtube.com/watch?v=FwOTs4UxQS4

---

## Summary

Jeff Su lays out a three-level framework for understanding AI systems: (1) LLMs — passive, limited to training data; (2) AI Workflows — a human programs fixed steps for an LLM with external tools, but it cannot deviate from those steps; (3) AI Agents — the LLM replaces the human as the decision-maker. The defining distinction: an AI agent is whatever system has an LLM in the decision-making role, regardless of the number of steps. The ReAct (Reason + Act) framework is the most common architectural pattern for agents. Autonomous iteration — the agent spawning additional LLM steps such as a critic to self-improve — is the third property that separates agents from workflows.

## Key Takeaways

- The single change turning a workflow into an agent: replacing the human decision-maker with an LLM
- LLMs have two core limitations: no access to proprietary data, and they are passive (only respond when prompted)
- AI Workflows overcome data limitations by giving LLMs predefined tool-access paths — but cannot deviate from those paths
- RAG is simply the mechanism for looking up external information — a type of AI workflow capability, not an agent capability by itself
- ReAct (Reason + Act) is the most common agent architectural pattern: reason → act via tools → observe → iterate
- Autonomous iteration is key: the agent can spawn a critic LLM step to self-improve without human intervention
- Number of steps is irrelevant — even thousands of steps remain a workflow if a human is the decision-maker at each branch

## Notable Quotes

> "The one massive change that has to happen for an AI workflow to become an AI agent is for me, the human decision maker, to be replaced by an LLM."

> "No matter how many steps we add, this is still just an AI workflow — if a human is the decision maker, there is no AI agent."

> "All AI agents must reason and act. So ReAct."

## Action Items

- [ ] Map your current AI usage against three levels (LLM / Workflow / Agent) to identify where human decision-making could be safely delegated
- [ ] When evaluating "AI agent" products, verify three properties: autonomous reasoning, tool-based action, and self-directed iteration
- [ ] Distinguish between workflow steps you hardcode vs. steps where the LLM decides dynamically
- [ ] Study the ReAct pattern as the baseline architecture for building your own agents
- [ ] Add a critic/evaluator LLM step to generative pipelines for autonomous quality iteration

## Key Terminology

| Term | Definition |
|------|-----------|
| AI Workflow | Automation where a human defines fixed steps for an LLM with external tools; cannot deviate from defined paths |
| AI Agent | System where LLM is the decision-maker: reasons about best approach, acts via tools, autonomously iterates |
| ReAct Framework | Reason + Act: agent reasons, acts using tools, observes result, decides whether to iterate further |
| Control Logic | Human-authored rules defining what an AI Workflow does at each step |
| RAG | Retrieval-Augmented Generation — looking up external data before answering; a type of AI Workflow |

---

## Related in This Session

- [Related: You're Not Behind (Yet): How to Build AI Agents in 2026](../reports/youre-not-behind-yet-how-to-build-ai-agents-in-2026.md) — both establish the agent vs. chatbot vs. workflow distinction for general audiences
- [Related: ИИ-агенты 2026: Конец программирования или новая эра?](../reports/ii-agenty-2026-konets-programmirovaniya-ili-novaya-era.md) — Russian counterpart covering the same definitional ground with risk and safety focus
- [Related: Don't Build Agents, Build Skills Instead — Anthropic](../reports/dont-build-agents-build-skills-instead-anthropic.md) — extends this conceptual foundation: given agents are defined, what domain expertise do they need?
- [Related: Top 6 AI Trends That Will Define 2026](../reports/top-6-ai-trends-that-will-define-2026.md) — Also from Jeff Su; applies agent concepts to broader 2026 trend analysis

---

## Резюме (Russian Summary)

**AI Agents, Clearly Explained**

Видео представляет трёхуровневую модель ИИ: LLM → AI Workflow → AI Agent. Ключевое отличие агента: замена человека как лица, принимающего решения, на LLM. Стандартный архитектурный паттерн — ReAct (Reason + Act).

### Ключевые выводы

- Единственное отличие Agent от Workflow: замена человека-решателя на LLM
- LLM пассивны и ограничены обучающими данными
- RAG — это паттерн воркфлоу, не признак агента
- ReAct: рассуждение → действие через инструменты → наблюдение → итерация
- Количество шагов не делает систему агентом — важно кто принимает решения
