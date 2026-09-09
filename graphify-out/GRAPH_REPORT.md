# Graph Report - Vanta-Deep-Research-API  (2026-09-10)

## Corpus Check
- 117 files · ~34,159 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 619 nodes · 1270 edges · 77 communities (41 shown, 12 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 140 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4ad100aa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- research.py
- LLMClient
- logging.py
- deliver_webhook_job
- run_research
- test_api_routes.py
- compilerOptions
- BaseExtractorPlugin
- decrypt
- package.json
- compilerOptions
- ToolRegistry
- dependencies
- App.tsx
- button.tsx
- test_research_submit.py
- test_smoke.py
- cli.py
- scripts
- Settings
- devDependencies
- tsconfig.json
- test_all_tables.py
- Vanta
- Endpoints
- migrate.py
- deep-research-api
- caveman/SKILL.md
- get_mode_config
- Detailed Workflow Analysis
- Installation
- Security Architecture
- Technology Stack
- Appendix
- Development Workflow
- Performance Considerations
- Observability
- test_modes_api.py
- test_db_engine.py
- Data Flow Architecture
- Deployment Architecture
- Roadmap
- Testing Strategy
- agents (caveman + graphify)
- Configuration
- Executive Summary
- Sequence Diagrams
- rules/agents.md
- rules/graphify.md
- workflows/agents.md
- workflows/graphify.md
- test_orgs_table.py
- MessageBus

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 55 edges
2. `Message` - 37 edges
3. `Vanta` - 31 edges
4. `LLMConfig` - 27 edges
5. `ResearchState` - 27 edges
6. `BaseAgent` - 24 edges
7. `run_research()` - 24 edges
8. `get_db_session()` - 24 edges
9. `ResearchJob` - 22 edges
10. `LLMResponse` - 18 edges

## Surprising Connections (you probably didn't know these)
- `chat_with_report()` --uses--> `LLMClient`  [INFERRED]
  api/routes/research.py → core/llm/client.py
- `chat_with_report()` --uses--> `LLMConfig`  [INFERRED]
  api/routes/research.py → core/llm/types.py
- `chat_with_report()` --uses--> `Message`  [INFERRED]
  api/routes/research.py → core/llm/types.py
- `search_knowledge_graph()` --uses--> `LLMClient`  [INFERRED]
  api/routes/research.py → core/llm/client.py
- `search_knowledge_graph()` --uses--> `LLMConfig`  [INFERRED]
  api/routes/research.py → core/llm/types.py

## Import Cycles
- None detected.

## Communities (77 total, 12 thin omitted)

### Community 0 - "research.py"
Cohesion: 0.06
Nodes (68): lifespan(), get, Request, read_index(), request_id_middleware(), audit_log_middleware(), Request, auth_middleware() (+60 more)

### Community 1 - "LLMClient"
Cohesion: 0.07
Nodes (61): LLMClient, call_anthropic(), call_openai(), embed_openai(), LLMConfig, LLMResponse, Message, BaseAgent (+53 more)

### Community 2 - "logging.py"
Cohesion: 0.40
Nodes (4): get_logger(), JSONFormatter, Logger, LogRecord

### Community 3 - "deliver_webhook_job"
Cohesion: 0.70
Nodes (4): deliver_webhook_job(), asyncio, test_webhook_delivery_failure_retry(), test_webhook_delivery_success()

### Community 4 - "run_research"
Cohesion: 0.15
Nodes (22): validate_source(), ValidatorAgent, run_research(), Event, fetch_url(), FetchedPage, _is_safe_url(), search_searxng() (+14 more)

### Community 5 - "test_api_routes.py"
Cohesion: 0.30
Nodes (15): hmac_sign(), _auth_patches(), _ctx(), _make_mock_key(), _make_mock_org(), asyncio, Patch auth + audit middleware DB calls., test_cancel_completed_job_returns_409() (+7 more)

### Community 6 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, allowSyntheticDefaultImports, esModuleInterop, forceConsistentCasingInFileNames, isolatedModules, jsx, lib (+10 more)

### Community 7 - "BaseExtractorPlugin"
Cohesion: 0.16
Nodes (9): ABC, BaseExtractorPlugin, BaseSearchPlugin, Execute a search. Returns a list of dictionaries with 'url', 'title', and…, Name of the extractor plugin (e.g., 'pdf', 'youtube')., Extract text content from the given URL., Name of the search plugin (e.g., 'google', 'arxiv')., PluginRegistry (+1 more)

### Community 8 - "decrypt"
Cohesion: 0.27
Nodes (14): decrypt(), encrypt(), _get_fernet(), Fernet, _ctx(), _make_api_key(), _make_org(), asyncio (+6 more)

### Community 9 - "package.json"
Cohesion: 0.16
Nodes (12): name, private, type, version, react-dom, tailwindcss, @tailwindcss/vite, @types/react (+4 more)

### Community 10 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, allowImportingTsExtensions, isolatedModules, lib, module, moduleDetection, moduleResolution, noEmit (+5 more)

### Community 11 - "ToolRegistry"
Cohesion: 0.23
Nodes (4): Any, Convert to a format suitable for LLM consumption (e.g. OpenAI tools format)., Tool, ToolRegistry

### Community 12 - "dependencies"
Cohesion: 0.17
Nodes (12): dependencies, class-variance-authority, clsx, lucide-react, react, react-dom, tailwind-merge, tailwindcss (+4 more)

### Community 13 - "App.tsx"
Cohesion: 0.22
Nodes (9): App(), CodeBlock(), features, navLinks, ModeOption, MODES, ResearchConsole(), lucide-react (+1 more)

### Community 14 - "button.tsx"
Cohesion: 0.31
Nodes (7): Button, ButtonProps, buttonVariants, cn(), class-variance-authority, clsx, tailwind-merge

### Community 15 - "test_research_submit.py"
Cohesion: 0.39
Nodes (7): _ctx(), _make_api_key(), _make_auth_session(), _make_org(), asyncio, A mock session that satisfies auth_middleware's two DB calls., test_submit_research_returns_202()

### Community 16 - "test_smoke.py"
Cohesion: 0.53
Nodes (5): e2e, asyncio, Smoke test against a live running stack. Set E2E_API_KEY and E2E_BASE_URL…, test_health_ready(), test_submit_and_poll_job()

### Community 17 - "cli.py"
Cohesion: 0.73
Nodes (5): list_modes_command(), main(), poll_job(), request_api(), submit_job()

### Community 18 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, build, dev, preview

### Community 19 - "Settings"
Cohesion: 0.67
Nodes (3): BaseSettings, Config, Settings

### Community 26 - "devDependencies"
Cohesion: 0.67
Nodes (3): devDependencies, @types/react, @types/react-dom

### Community 29 - "Vanta"
Cohesion: 0.10
Nodes (20): Agent Specifications, Architectural Principles, CI/CD Pipeline, Component Responsibility Table, Contributing, Data Retention Policy, Database Design, Developer CLI (+12 more)

### Community 30 - "Endpoints"
Cohesion: 0.15
Nodes (13): API Documentation, Endpoints, Error Codes, `GET /v1/research/{job_id}` (completed), Knowledge Graph, `POST /v1/research`, Reports, Request & Response Examples (+5 more)

### Community 50 - "caveman/SKILL.md"
Cohesion: 0.17
Nodes (10): caveman, Example output, How to invoke, See also, What it does, Auto-Clarity, Boundaries, Intensity (+2 more)

### Community 51 - "get_mode_config"
Cohesion: 0.22
Nodes (10): get_mode_config(), list_available_modes(), ModeConfig, Resolve ModeConfig by name, fallback to standard research mode if invalid or…, Return list of serialized mode metadata for API and CLI consumption., ResearchMode, Enum, str (+2 more)

### Community 52 - "Detailed Workflow Analysis"
Cohesion: 0.29
Nodes (7): 1. Job Submission Flow, 2. Worker Execution Flow, 3. Research Engine Loop, 4. Webhook Delivery Flow, 5. Report Export Flow, 6. Error Handling Flow, Detailed Workflow Analysis

### Community 53 - "Installation"
Cohesion: 0.33
Nodes (6): Air-Gap / Fully Offline Setup, Docker Setup (Recommended), Installation, Local Development Setup, Prerequisites, Verification

### Community 54 - "Security Architecture"
Cohesion: 0.33
Nodes (6): Audit Log, Authentication Model, Provider Auto-Detection Logic, Secrets at Rest, Security Architecture, Security Controls Summary

### Community 55 - "Technology Stack"
Cohesion: 0.33
Nodes (6): Backend, CI/CD, Database & Storage, Frontend, Infrastructure, Technology Stack

### Community 56 - "Appendix"
Cohesion: 0.40
Nodes (5): Appendix, Glossary, LLM Provider Support Matrix, References, State & Storage Map

### Community 57 - "Development Workflow"
Cohesion: 0.40
Nodes (5): Branching Strategy, Code Standards, Commit Conventions, Development Workflow, Pull Request Process

### Community 58 - "Performance Considerations"
Cohesion: 0.40
Nodes (5): Caching, Context Window Management, Fetch Concurrency, LLM Call Budget Per Job, Performance Considerations

### Community 59 - "Observability"
Cohesion: 0.40
Nodes (5): Distributed Tracing (Planned), Health Endpoints, Logging, Metrics, Observability

### Community 60 - "test_modes_api.py"
Cohesion: 0.60
Nodes (4): _ctx(), asyncio, test_get_modes_endpoint(), test_submit_research_with_mode()

### Community 62 - "Data Flow Architecture"
Cohesion: 0.50
Nodes (4): Data Flow Architecture, Ingestion Pipeline, Knowledge Graph (pgvector), Storage Architecture

### Community 63 - "Deployment Architecture"
Cohesion: 0.50
Nodes (4): Deployment Architecture, Local / Development, Production (Kubernetes — Planned), Scaling Strategy

### Community 64 - "Roadmap"
Cohesion: 0.50
Nodes (4): Long-Term, Medium-Term (v0.4–0.5), Near-Term (v0.3), Roadmap

### Community 65 - "Testing Strategy"
Cohesion: 0.50
Nodes (4): Mocking Conventions, Running Tests, Test Coverage Expectations, Testing Strategy

### Community 68 - "Configuration"
Cohesion: 0.67
Nodes (3): Configuration, Core Settings, Docker Compose Variables (deploy/.env)

### Community 69 - "Executive Summary"
Cohesion: 0.67
Nodes (3): Executive Summary, Who It Is For, Why It Exists

### Community 70 - "Sequence Diagrams"
Cohesion: 0.67
Nodes (3): Full Research Job Lifecycle, Sequence Diagrams, Webhook Retry Sequence

## Knowledge Gaps
- **156 isolated node(s):** `Config`, `name`, `private`, `version`, `type` (+151 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 256 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `research.py`, `run_research`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `Vanta` connect `Vanta` to `Roadmap`, `Testing Strategy`, `Configuration`, `Executive Summary`, `Sequence Diagrams`, `Detailed Workflow Analysis`, `Installation`, `Security Architecture`, `Endpoints`, `Appendix`, `Development Workflow`, `Performance Considerations`, `Observability`, `Technology Stack`, `Data Flow Architecture`, `Deployment Architecture`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `run_research_job()` connect `research.py` to `decrypt`, `LLMClient`, `run_research`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `LLMClient` (e.g. with `chat_with_report()` and `search_knowledge_graph()`) actually correct?**
  _`LLMClient` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `Message` (e.g. with `chat_with_report()` and `LLMClient`) actually correct?**
  _`Message` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `LLMConfig` (e.g. with `chat_with_report()` and `search_knowledge_graph()`) actually correct?**
  _`LLMConfig` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `ResearchState` (e.g. with `CitationVerifierAgent` and `verify_citations()`) actually correct?**
  _`ResearchState` has 13 INFERRED edges - model-reasoned connections that need verification._