# DevRel Agent

An AI-powered Developer Relations agent built on [Deep Agents](https://github.com/langchain-ai/deep-agents) that helps developers understand codebases, APIs, and SDKs through interactive teaching.

## Architecture

```
┌──────────────────────────────────────────────┐
│        DevRel Orchestrator Agent              │
│  (TodoList + Memory + Filesystem + Skills)    │
├──────────────────┬───────────────────────────┤
│  SubAgent:       │  SubAgent:                │
│  Architecture    │  Code Example             │
│  Explainer       │  Generator                │
└──────────────────┴───────────────────────────┘
```

- **Orchestrator** — plans exploration, delegates to subagents, remembers context across sessions
- **Architecture Explainer** — reads source code and produces layered explanations (bird's eye → module → flow)
- **Code Example Generator** — creates annotated, runnable code samples

## Tech Stack

- **Backend**: Python, FastAPI, Deep Agents (LangChain/LangGraph)
- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **LLM**: Claude Sonnet (configurable)

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- An Anthropic API key (or OpenAI)

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key and target repo path
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Running

Start the backend:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Start the frontend:
```bash
cd frontend
npm run dev
```

Open http://localhost:5173 and start asking about the target codebase.

## Configuration

Set these in `backend/.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | (required) |
| `OPENAI_API_KEY` | Your OpenAI API key (alternative) | (optional) |
| `TARGET_REPO_PATH` | Path to the repo the agent will analyze | `./sample-repo` |

## Skills

Skills are loaded on-demand by the agent from `backend/skills/`:

- **architecture-explainer** — Generates layered architecture explanations for junior developers
- **code-example-style** — Produces annotated, runnable code samples with progressive complexity

## Project Structure

```
dev-rel-agent/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI server
│   │   ├── agent.py          # Deep Agents orchestrator + subagents
│   │   ├── tools.py          # Custom repo-reading tools
│   │   └── subagents/        # (extensible)
│   ├── skills/
│   │   ├── architecture-explainer/
│   │   │   └── SKILL.md
│   │   └── code-example-style/
│   │       └── SKILL.md
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # Main chat UI
│   │   ├── api.ts            # Backend API client
│   │   └── components/
│   │       ├── ChatMessage.tsx
│   │       ├── ChatInput.tsx
│   │       └── TodoPanel.tsx
│   └── package.json
└── README.md
```

## Roadmap

- **Phase 1 (current)**: Interactive teaching agent — architecture explanations + code examples
- **Phase 2**: Content generation — blog posts, tutorials, social media copy with HITL review
