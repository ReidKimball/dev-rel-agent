"""Custom tools for reading target repository files."""

import os
from pathlib import Path
from typing import Optional

from langchain.tools import tool


def create_repo_tools(repo_path: str):
    """Create tools scoped to a specific target repository path."""

    root = Path(repo_path).resolve()

    @tool
    def list_repo_files(directory: str = ".") -> str:
        """List files and directories in the target repository.
        Use '.' for the root directory or provide a relative path."""
        target = (root / directory).resolve()
        if not str(target).startswith(str(root)):
            return "Error: Cannot access paths outside the target repository."
        if not target.exists():
            return f"Error: Directory '{directory}' not found."
        if not target.is_dir():
            return f"Error: '{directory}' is not a directory."

        entries = []
        for entry in sorted(target.iterdir()):
            rel = entry.relative_to(root)
            if entry.is_dir():
                entries.append(f"[DIR]  {rel}/")
            else:
                size = entry.stat().st_size
                entries.append(f"[FILE] {rel} ({size} bytes)")
        return "\n".join(entries) if entries else "(empty directory)"

    @tool
    def read_repo_file(file_path: str) -> str:
        """Read a file from the target repository. Provide a relative path."""
        target = (root / file_path).resolve()
        if not str(target).startswith(str(root)):
            return "Error: Cannot access paths outside the target repository."
        if not target.exists():
            return f"Error: File '{file_path}' not found."
        if not target.is_file():
            return f"Error: '{file_path}' is not a file."
        try:
            content = target.read_text(encoding="utf-8", errors="replace")
            if len(content) > 50_000:
                content = content[:50_000] + "\n\n... (truncated, file too large)"
            return content
        except Exception as e:
            return f"Error reading file: {e}"

    @tool
    def search_repo(pattern: str, file_glob: Optional[str] = None) -> str:
        """Search for a text pattern across files in the target repository.
        Optionally filter by file glob (e.g. '*.py', '*.ts')."""
        results = []
        for path in root.rglob(file_glob or "*"):
            if not path.is_file():
                continue
            if any(part.startswith(".") for part in path.parts):
                continue
            if path.suffix in {".pyc", ".pyo", ".so", ".dll", ".exe", ".bin"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
                for i, line in enumerate(text.splitlines(), 1):
                    if pattern.lower() in line.lower():
                        rel = path.relative_to(root)
                        results.append(f"{rel}:{i}: {line.strip()}")
                        if len(results) >= 50:
                            results.append("... (results truncated at 50 matches)")
                            return "\n".join(results)
            except Exception:
                continue
        return "\n".join(results) if results else f"No matches found for '{pattern}'."

    return [list_repo_files, read_repo_file, search_repo]
