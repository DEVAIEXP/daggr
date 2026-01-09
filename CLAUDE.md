# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Code Style

- AVOID inline comments in code!!!

## Commands

### Development Setup
```bash
# Install with development dependencies
pip install -e .[dev]
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_example.py
```

### Code Formatting and Linting
```bash
# Format and lint code (required before commits)
ruff check --fix --select I && ruff format
```

## Architecture Overview

daggr is a DAG-based workflow library for connecting Gradio apps, ML models, and custom functions.

### Core Components

- **`context.py`**: Context management using `contextvars` for tracking the current Graph (similar to Gradio Blocks)
- **`graph.py`**: Main `Graph` class with context manager support and DAG validation using networkx
- **`node.py`**: Node types (`GradioNode`, `InferenceNode`, `FnNode`, `InteractionNode`) with port access via `__getitem__`
- **`port.py`**: `Port` class representing input/output ports, supports `>>` operator for edge creation
- **`edge.py`**: `Edge` class that auto-registers nodes with the current graph context
- **`ops.py`**: Special operation nodes like `ChooseOne`, `TextInput`, `ImageInput`
- **`executor.py`**: Sequential execution of workflow nodes
- **`ui.py`**: Generates Gradio UI from the workflow graph

### Key Design Patterns

1. **Context Manager Pattern**: `with Graph() as graph:` sets up context for edge creation
2. **Operator Overloading**: `>>` operator creates edges between ports/nodes
3. **Auto-registration**: Nodes are automatically added to the graph when edges are created
4. **Port Resolution**: `node["port_name"]` returns a `Port` object; shorthand `node >> node` uses default ports

### Example Usage
```python
from daggr import Graph, GradioNode, FnNode, ops

def process(text: str) -> dict:
    return {"result": text.upper()}

node1 = FnNode(fn=process)
node2 = GradioNode(src="gradio/gpt2")

with Graph() as graph:
    node1["result"] >> node2["input"]

graph.launch()
```

### Testing Strategy

Tests are located in the `tests/` directory. The `conftest.py` provides shared fixtures. Always run tests before committing changes.

### Important Files for Common Tasks

- **Adding new node types**: Modify `daggr/node.py`
- **Adding new operations**: Modify `daggr/ops.py`
- **Modifying UI generation**: Update `daggr/ui.py`
- **Adding dependencies**: Update `pyproject.toml` under `[project.dependencies]`

## Issue Resolution Workflow

When given a GitHub issue to solve, follow this workflow:

1. **Create a new branch** named after the issue (e.g., `fix-issue-123` or descriptive name)
2. **Implement the solution** following the existing code patterns and conventions
3. **Run tests** to ensure nothing is broken: `pytest`
4. **Run linting/formatting**: `ruff check --fix --select I && ruff format`
5. That's it. Never use the `git` commit command after a task is finished.

### Git Commands for Issue Workflow
```bash
git checkout -b fix-issue-NUMBER
```

Always ensure tests pass and code is formatted before pushing.
