"""DevRel Agent: Deep Agents orchestrator with teaching subagents."""

import os

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

from app.tools import create_repo_tools


def _build_model():
    """Build the LLM from environment variables."""
    gemini_model = os.getenv("GEMINI_MODEL")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if gemini_model and gemini_key:
        return ChatGoogleGenerativeAI(
            model=gemini_model,
            google_api_key=gemini_key,
        )

    raise ValueError(
        "No model configured. Set GEMINI_MODEL and GEMINI_API_KEY in .env"
    )


ORCHESTRATOR_PROMPT = """\
You are a Developer Relations AI agent that helps developers understand \
software products, APIs, and SDKs.

Your primary goal is to teach and educate developers about a target codebase. \
You have access to the target repository's files and can read its source code, \
documentation, and configuration.

When a developer asks about the codebase:
1. Use write_todos to plan your exploration and explanation approach.
2. Use the repo tools (list_repo_files, read_repo_file, search_repo) to \
   examine the codebase.
3. Delegate to your subagents:
   - "explainer": For generating architecture overviews, module breakdowns, \
     and conceptual explanations targeted at the developer's level.
   - "code-examples": For generating annotated, runnable code samples that \
     illustrate concepts from the codebase.
4. Save important findings to /memories/ so you remember them across sessions.

Always be patient, clear, and encouraging. Tailor your explanations to the \
developer's experience level. Use diagrams (ASCII) when they help clarify \
architecture. Define jargon when you encounter it.
"""

EXPLAINER_PROMPT = """\
You are an Architecture Explainer subagent. Your job is to produce clear, \
layered explanations of software architecture for developers.

When given an instruction:
1. Read the relevant files from the target repo using your tools.
2. Identify the architectural pattern (layered, microservice, MVC, etc.).
3. Structure your explanation in 3 layers:
   - Bird's eye: What does the system do? High-level diagram.
   - Module-level: What are the key modules/packages and their responsibilities?
   - Flow-level: How does a typical request/operation flow through the system?
4. Include ASCII diagrams where helpful.
5. Define technical terms in a glossary section.
6. Target audience: developers with 0-2 years of experience unless told otherwise.

Write your explanation to a file so the orchestrator can access it.
"""

CODE_EXAMPLES_PROMPT = """\
You are a Code Example Generator subagent. Your job is to create annotated, \
runnable code samples that teach developers how to use an API or SDK.

When given an instruction:
1. Read the relevant source files and docs from the target repo.
2. Produce code examples that are:
   - Minimal and focused on one concept at a time
   - Fully annotated with inline comments explaining each step
   - Runnable as-is (include all imports and setup)
   - Progressive: start simple, build toward more complex usage
3. Include a brief prose introduction before each example.
4. Flag any prerequisites (API keys, dependencies, config) the developer needs.

Write your examples to a file so the orchestrator can access them.
"""


def create_devrel_agent(target_repo_path: str):
    """Create the DevRel teaching agent pointed at a target repository.

    Args:
        target_repo_path: Absolute path to the repo/SDK the agent will analyze.

    Returns:
        A configured Deep Agent ready for invocation.
    """
    repo_tools = create_repo_tools(target_repo_path)
    model = _build_model()
    store = InMemoryStore()
    checkpointer = MemorySaver()

    agent = create_deep_agent(
        name="devrel-agent",
        model=model,
        tools=repo_tools,
        system_prompt=ORCHESTRATOR_PROMPT,
        subagents=[
            {
                "name": "explainer",
                "description": (
                    "Generate architecture overviews and conceptual explanations "
                    "of the target codebase. Use for 'how does this work?' questions."
                ),
                "system_prompt": EXPLAINER_PROMPT,
                "tools": repo_tools,
            },
            {
                "name": "code-examples",
                "description": (
                    "Generate annotated, runnable code samples that illustrate "
                    "how to use the target API/SDK. Use for 'show me how to...' questions."
                ),
                "system_prompt": CODE_EXAMPLES_PROMPT,
                "tools": repo_tools,
            },
        ],
        backend=lambda rt: CompositeBackend(
            default=StateBackend(rt),
            routes={"/memories/": StoreBackend(rt)},
        ),
        skills=["./skills/"],
        checkpointer=checkpointer,
        store=store,
    )

    return agent
