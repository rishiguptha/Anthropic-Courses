# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf

# Install package in development mode
uv pip install -e .
```

## Architecture

This is an MCP server that exposes document-processing tools to AI assistants via the [Model Context Protocol](https://modelcontextprotocol.io).

**Entry point** (`main.py`): Creates a `FastMCP` instance, imports tool functions from `tools/`, registers each with `mcp.tool()(fn)`, then calls `mcp.run()`.

**`tools/`**: Plain Python functions with no MCP dependencies. Each tool is a standalone function that can be tested independently. Currently:
- `tools/math.py` — `add`: example numeric tool
- `tools/document.py` — `binary_document_to_markdown`: converts binary PDF/DOCX data to markdown using `markitdown`

**`tests/`**: pytest suite. Fixtures (sample `.pdf` and `.docx` files) live in `tests/fixtures/`.

## Defining MCP Tools

Tools are plain Python functions registered in `main.py` via `mcp.tool()(fn)`. Use `pydantic.Field` for parameter descriptions:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of functionality.

    When to use:
    - Describe appropriate use cases
    - Describe when NOT to use

    Examples:
    >>> my_tool("foo", 42)
    "expected output"
    """
    # Implementation
```

After defining a tool function in `tools/`, register it in `main.py`:

```python
from tools.my_module import my_tool
mcp.tool()(my_tool)
```

Tool docstrings drive the descriptions exposed to AI clients — be specific about behavior, edge cases, and examples.

## Code Style

- Always apply explicit type annotations to all function arguments and return values.
