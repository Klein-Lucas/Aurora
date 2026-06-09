# aurora

> A minimalist CLI task manager — fast, clean, and built for the terminal.

## About

**aurora** is a command-line tool to create, view, update, and delete tasks directly from the terminal. Built with [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/), it combines a simple interface with a visually polished output.

## Tech Stack

- **Python** 3.11+
- **Typer** — CLI framework
- **Rich** — colored tables and terminal output
- **uv** — package and environment manager
- **pytest** — automated tests

## Installation

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/Klein-Lucas/aurora_root.git
cd aurora_root

uv venv
uv sync
```

## Usage

All commands run with `python -m aurora.cli <command>`.

### Create a task

```bash
python -m aurora.cli create "Study Python" --description "Review chapter 5" --category study --end-date 2026-06-15
```

### List tasks

```bash
python -m aurora.cli show
```

```
           Tasks
┌───────┬───────────────┬────────────┐
│ Index │ Title         │ Status     │
├───────┼───────────────┼────────────┤
│ 1     │ Study Python  │ new        │
└───────┴───────────────┴────────────┘
```

### Update a task

```bash
python -m aurora.cli update 1 --status in_progress
```

### Delete a task

```bash
python -m aurora.cli delete 1
```

## Task Fields

| Field         | Type     | Description                                    |
|---------------|----------|------------------------------------------------|
| `title`       | required | Task name                                      |
| `description` | optional | Additional details                             |
| `start-date`  | optional | Start date (`YYYY-MM-DD`)                      |
| `end-date`    | optional | Deadline (`YYYY-MM-DD`)                        |
| `category`    | optional | `work`, `study`, `health`, `hobby`             |
| `status`      | optional | `new`, `in_progress`, `done`, `deleted`        |

## Project Structure

```
src/aurora/
├── cli.py        # CLI commands (Typer)
├── crud.py       # Create, read, update, delete operations
├── storage.py    # JSON persistence layer
├── task.py       # Data model (dataclass + enums)
└── exceptions.py # Custom exceptions
tests/
└── crud_test.py  # Automated tests
```

## Running Tests

```bash
uv run pytest tests/
```

## License

MIT