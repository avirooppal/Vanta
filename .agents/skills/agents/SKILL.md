---
name: agents
description: Combined workflow skill that activates caveman ultra-compressed communication and queries the codebase with graphify knowledge graph. Use for /agents or "use /agents".
---

# agents (caveman + graphify)

Unified mode combining **caveman** (ultra-terse compression) and **graphify** (knowledge graph intelligence).

## When Triggered (`/agents`, `use /agents`)

1. **Adopt Caveman Style**:
   - Ultra-compressed communication (default: level full).
   - Omit articles (a, an, the), pleasantries, filler words.
   - Retain complete technical substance, exact code symbols, paths, and shell commands.
   - Direct facts: `[thing] [action] [reason]. [next step].`

2. **Query with Graphify**:
   - Check if `graphify-out/graph.json` exists in project root.
   - If not found, run `graphify .` to build the AST and semantic graph.
   - For queries: run `graphify query "<question>"`, `graphify explain "<concept>"`, or `graphify path "<A>" "<B>"`.
   - If files change: run `graphify update .`.

3. **Response Structure**:
   - Graph-grounded findings presented with zero filler.
