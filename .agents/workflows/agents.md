---
name: agents
description: Execute tasks and query the codebase combining caveman compression mode and graphify knowledge graph
---

# Workflow: /agents

When `/agents` is invoked (e.g. `/agents <query>` or `use /agents`):

1. **Activate Caveman Mode**:
   - Follow instructions in `.agents/skills/caveman/SKILL.md`.
   - Terse, dense, smart caveman tone. All technical substance stays; only fluff and filler die.
   - Drop articles (a/an/the), pleasantries, hedging. Active voice, fragments OK.
   - Retain exact code blocks, commands, and numbers.
   - Default level: **full**.

2. **Ground Answers in Graphify Knowledge Graph**:
   - Follow instructions in the `graphify` skill.
   - If `graphify-out/graph.json` does not exist:
     - Run `graphify .` (or invoke the `graphify` skill) to build the knowledge graph.
   - If `graphify-out/graph.json` exists:
     - Codebase / architecture questions: run `graphify query "<question>"`.
     - Concept definitions / node inspection: run `graphify explain "<concept>"`.
     - Relationships / data flow / call paths: run `graphify path "<nodeA>" "<nodeB>"`.
     - If code was modified in the session: run `graphify update .`.

3. **Output Format**:
   - Deliver Graphify insights formatted in Caveman style: high token efficiency, direct answers, zero preamble.
