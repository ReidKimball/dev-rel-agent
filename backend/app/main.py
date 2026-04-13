"""FastAPI server for the DevRel Agent."""

import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agent import create_devrel_agent

load_dotenv()

app = FastAPI(title="DevRel Agent API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent on startup
TARGET_REPO = os.getenv("TARGET_REPO_PATH", "./sample-repo")
agent = None


@app.on_event("startup")
async def startup():
    global agent
    repo_path = os.path.abspath(TARGET_REPO)
    if not os.path.isdir(repo_path):
        print(f"WARNING: Target repo path '{repo_path}' does not exist. Creating it.")
        os.makedirs(repo_path, exist_ok=True)
    agent = create_devrel_agent(repo_path)
    print(f"DevRel Agent initialized. Target repo: {repo_path}")


class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    thread_id: str
    todos: list[dict] | None = None


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config=config,
        )

        # Extract the assistant's last message
        # Use .text property which always returns a plain string,
        # regardless of whether the provider returns content as
        # a string or a list of content blocks.
        messages = result.get("messages", [])
        assistant_msg = ""
        for msg in reversed(messages):
            if hasattr(msg, "type") and msg.type == "ai":
                assistant_msg = msg.text if hasattr(msg, "text") else str(msg.content)
                break
            elif isinstance(msg, dict) and msg.get("role") == "assistant":
                assistant_msg = msg.get("content", "")
                break

        todos = result.get("todos", [])

        return ChatResponse(
            response=assistant_msg or "I couldn't generate a response.",
            thread_id=thread_id,
            todos=todos if todos else None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "target_repo": os.path.abspath(TARGET_REPO),
        "agent_ready": agent is not None,
    }
