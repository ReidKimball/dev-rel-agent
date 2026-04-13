---
name: code-example-style
description: Generate annotated, runnable code examples that teach developers how to use an API or SDK. Use when asked to show usage examples, create quickstart samples, or demonstrate specific features.
---

# Code Example Style Guide

## Overview
Produces clear, annotated, runnable code samples that teach developers how to use an API, SDK, or library. Each example should be copy-pasteable and work immediately.

## When to Use
- User asks "how do I use X?"
- User asks for a code example or quickstart
- User wants to see a specific feature in action
- User asks "show me how to..."

## Instructions

### Structure Each Example

```
1. Title (what this example demonstrates)
2. Prerequisites (1-2 lines: what you need installed/configured)
3. Brief prose introduction (2-3 sentences: what we're building and why)
4. The code (fully annotated)
5. Expected output (what the developer should see when they run it)
6. What to try next (one suggestion for extending the example)
```

### Code Annotation Rules
- Add a comment before each logical block explaining WHAT it does and WHY
- Do NOT comment every single line — that's noise
- Use the pattern: blank line → comment → code block
- Example:
  ```python
  # Set up the client with your API key.
  # The client handles authentication and retry logic automatically.
  client = APIClient(api_key=os.environ["API_KEY"])

  # Fetch the first 10 users. The response is paginated by default.
  users = client.users.list(limit=10)
  ```

### Progressive Complexity
When generating multiple examples, order them:
1. **Hello World** — simplest possible usage (3-10 lines)
2. **Common Use Case** — the thing most developers will actually do
3. **Advanced Pattern** — error handling, configuration, edge cases

### Completeness Checklist
- [ ] All imports included at the top
- [ ] All environment variables / config values noted
- [ ] No placeholder values without explanation (e.g., `"YOUR_API_KEY"` with a comment on where to get it)
- [ ] Code runs as-is when prerequisites are met
- [ ] Language-appropriate style (PEP 8 for Python, Prettier defaults for JS/TS)

### Tone
- Conversational but precise
- "Let's start by..." not "The following code demonstrates..."
- Acknowledge when something is tricky: "This part is a bit subtle — here's why..."
