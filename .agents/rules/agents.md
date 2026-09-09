---
trigger: always_on
description: Activate caveman mode and consult graphify knowledge graph whenever /agents or "use /agents" is invoked.
---

## /agents Rule: Caveman + Graphify

When the user writes `/agents` or says "use /agents":
1. **Caveman Style Active**:
   - Speak like smart caveman (per `caveman` skill).
   - High information density, drop articles, filler, pleasantries, hedging.
   - Technical substance, exact code, paths, and commands stay verbatim.
2. **Graphify for Codebase & Architecture**:
   - Use `graphify-out/` knowledge graph for code and architecture analysis (per `graphify` skill).
   - If `graphify-out/graph.json` does not exist, build it first with `graphify .`.
   - Query graph using `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"`.
   - Keep graph in sync using `graphify update .` after changes.
3. **Synthesis**:
   - Combine Graphify graph-grounded facts with Caveman terse delivery.
