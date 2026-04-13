---
name: architecture-explainer
description: Explain SDK or API system architecture to junior developers. Use when asked to break down how a codebase, API, or SDK is structured, or when onboarding a developer onto an unfamiliar project.
---

# Architecture Explainer

## Overview
Generates beginner-friendly, layered explanations of system architecture by reading source code, documentation, and configuration files from the target repository.

## When to Use
- User asks "how does this SDK/API work?"
- User asks for an architecture overview or diagram
- User is onboarding onto an unfamiliar codebase
- User asks "what does this module/package do?"

## Instructions

### Step 1: Survey the Project
- Use `list_repo_files` to scan the top-level directory structure
- Identify key directories: src/, lib/, api/, config/, tests/, docs/
- Read the README, package.json/pyproject.toml/Cargo.toml for project metadata

### Step 2: Identify Entry Points
- Find the main entry point (main.py, index.ts, App.java, etc.)
- Trace the initialization flow: what gets set up on startup?
- Note any configuration files or environment variable usage

### Step 3: Map the Architecture
- Identify the architectural pattern: layered, MVC, microservice, plugin, event-driven, etc.
- List the key modules/packages and their single-sentence purpose
- Map dependencies between modules (what calls what)

### Step 4: Write the Explanation (3 Layers)

#### Layer 1 — Bird's Eye View
- One paragraph: what does this system do?
- ASCII diagram showing the major components and how they connect
- Analogy if helpful (e.g., "Think of it like a restaurant: the router is the host, the controller is the waiter...")

#### Layer 2 — Module Breakdown
- For each key module:
  - **What it does** (one sentence)
  - **Key files** (2-3 most important)
  - **How it connects** to other modules

#### Layer 3 — Request/Operation Flow
- Pick the most common operation (e.g., "user makes an API call")
- Trace it step-by-step through the codebase
- Show which files/functions are involved at each step

### Step 5: Glossary
- Define any domain-specific terms or jargon encountered
- Keep definitions to one sentence each

### Tone & Audience
- Default target: developer with 0-2 years experience
- Use "you" language: "When you call this endpoint, the router sends your request to..."
- Avoid unnecessary jargon; when technical terms are needed, define them inline
- Be encouraging: "This might look complex, but it follows a simple pattern..."
