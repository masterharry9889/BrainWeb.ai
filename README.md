# BrainWeb.ai

**Live site:** [https://brainwebai.vercel.app/](https://brainwebai.vercel.app/)

BrainWeb.ai is a multi-agent AI workspace that runs specialized LLM agents against user inputs and automatically weaves their outputs into a live, explorable knowledge graph. Every agent run streams tokens in real time over WebSockets, and every entity or relation an agent extracts is written directly onto a shared graph that can be inspected, edited, and grown over time.

The application ships as both a web app (FastAPI + Next.js) and a native desktop app (Electron). It is bring-your-own-key: users supply a provider API key (Anthropic, OpenAI, or Groq), and BrainWeb.ai routes agent calls through it via [LiteLLM](https://github.com/BerriAI/litellm).

> This repository contains the core product: the FastAPI backend, the in-app Next.js frontend (graph canvas and agent runner UI), and the Electron desktop shell. The marketing site at [https://brainwebai.vercel.app/](https://brainwebai.vercel.app/) is maintained in a separate repository: [BrainWeb-frontend-](https://github.com/masterharry9889/BrainWeb-frontend-).

## How It Works

1. **Pick or define an agent.** BrainWeb.ai ships with built-in agents (e.g. a Research Agent and a Legal Doc Reviewer) and supports custom agents with a user-defined system prompt, input/output schema, and tools.
2. **Run it.** A run is dispatched as a background task and streamed back over a per-run WebSocket channel (`run.started` → `run.token` → `run.finished` / `run.error`), allowing the frontend to render tokens as they arrive.
3. **Extraction, not just chat.** Every agent is prompted to close its response with a structured JSON block of entities and relations. The orchestrator parses that block out of the streamed response even when the model omits proper fencing.
4. **Graph writer.** A background `graph_writer` service consumes finished runs and merges the extracted entities and relations into a persistent graph (`nodes` / `edges` tables), scoped per `project_id`, with mention counts and edge weights so the graph strengthens with continued use.
5. **Visualize and edit.** The Next.js frontend renders the graph with `@xyflow/react` and `react-force-graph-2d`, allowing nodes and edges to be inspected, renamed, merged, or deleted directly.

## Tech Stack

| Layer | Stack |
|---|---|
| Backend | FastAPI, SQLAlchemy (async), Pydantic, WebSockets, LiteLLM |
| Database | SQLite (`aiosqlite`) by default for local development; `docker-compose.yml` provisions Postgres (`pgvector/pgvector`) and Redis for a production-style setup |
| Frontend | Next.js 16, React 19, TypeScript, `@xyflow/react`, `react-force-graph-2d`, `react-markdown` |
| Desktop | Electron, wrapping the built Next.js static export and a PyInstaller-built FastAPI binary as a thin client |
| Auth to LLMs | Bring-your-own-key, encrypted at rest (`cryptography`), routed through LiteLLM to Anthropic, OpenAI, or Groq |

## Project Structure

```
BrainWeb.ai/
├── backend/
│   ├── main.py              # FastAPI app entrypoint + lifespan (DB init, graph writer task)
│   ├── models.py            # SQLAlchemy models: UserSettings, CustomAgent, Node, Edge
│   ├── database.py          # Async engine/session (SQLite by default, DATABASE_URL override)
│   ├── api/routes.py        # REST + WebSocket routes (agents, runs, settings, graph)
│   ├── core/
│   │   ├── orchestrator.py  # Built-in agents + LiteLLM-backed run loop
│   │   ├── schemas.py       # Pydantic request/response schemas
│   │   └── security.py      # API key encryption/decryption/masking
│   ├── services/
│   │   ├── graph_writer.py  # Background consumer that writes agent output into the graph
│   │   └── pubsub.py        # Event pub/sub backing the run WebSocket stream
│   └── build.py, *.spec     # PyInstaller packaging for the desktop build
├── frontend/                # Next.js app (graph canvas, agent runner UI, settings)
├── desktop/                 # Electron shell that wraps the frontend + bundled backend binary
└── docker-compose.yml       # Postgres (pgvector) + Redis for a hosted-style setup
```

## API Overview

- `GET /agents` · `POST/PUT/DELETE /agents/custom/{id}` — list built-in agents, manage custom ones
- `POST /agents/run` — start an agent run, returns a `run_id`
- `WS /runs/{run_id}` — stream `run.started` / `run.token` / `run.finished` / `run.error` events
- `GET/POST/DELETE /settings` — manage provider API keys
- `GET/DELETE /graph/{project_id}` — read or clear the knowledge graph for a project
- `GET/PUT /graph/node/{node_id}` — inspect or edit a single node and its edges

## License

GPL-3.0. See [`LICENSE`](./LICENSE).
