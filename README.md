# Aurora

> A minimalist task manager — usable both as a terminal CLI and as a REST API.

## About

**Aurora** lets you create, view, update, and delete tasks. It started as a CLI built with [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/), and now also exposes a [FastAPI](https://fastapi.tiangolo.com/) HTTP API. Both interfaces share the same core: a `Task` model, a storage-agnostic CRUD layer, and a SQLite-backed storage implementation.

This is a personal portfolio project built to practice and showcase backend engineering fundamentals — clean architecture, typed data validation, automated testing, and REST API design — with a React frontend currently in development on a separate branch.

## Highlights

- **Storage-agnostic architecture** — a `Protocol`-based interface decouples business logic from persistence, allowing SQLite and JSON backends to be swapped without touching the CRUD layer
- **Two interfaces, one core** — CLI and REST API reuse the same `Task` model, CRUD layer, and validation logic instead of duplicating business rules
- **Type-safe data validation** with Pydantic models and enums shared across both interfaces
- **Automated test coverage** with `pytest`, including FastAPI's `TestClient` for API-level tests
- **Incremental delivery** via feature branches and pull requests, tracked in the [Roadmap](#roadmap) below

## Tech Stack

- **Python** 3.11+
- **Typer** — CLI framework
- **Rich** — colored tables and terminal output
- **FastAPI** + **Uvicorn** — REST API and ASGI server
- **Pydantic** — data validation and schemas
- **SQLite** — persistence
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

### CLI

All commands run with `python -m aurora.cli <command>`.

#### Create a task

```bash
python -m aurora.cli create "Study Python" --description "Review chapter 5" --category study --end-date 2026-06-15
```

#### List tasks

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

#### Update a task

```bash
python -m aurora.cli update 1 --status in_progress
```

#### Delete a task

```bash
python -m aurora.cli delete 1
```

### API

Start the server:

```bash
uv run uvicorn aurora.main:app --reload
```

Interactive docs are available at `http://127.0.0.1:8000/docs`.

| Method | Endpoint      | Description       |
|--------|---------------|--------------------|
| POST   | `/tasks`      | Create a task      |
| GET    | `/tasks`      | List all tasks     |
| GET    | `/tasks/{id}` | Get a task by id   |
| PATCH  | `/tasks/{id}` | Update a task      |
| DELETE | `/tasks/{id}` | Delete a task      |

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Study Python", "category": "study", "end_date": "2026-06-15"}'
```

## Task Fields

| Field         | Type     | Description                                    |
|---------------|----------|------------------------------------------------|
| `title`       | required | Task name                                      |
| `description` | optional | Additional details                             |
| `start_date`  | optional | Start date (`YYYY-MM-DD`)                      |
| `end_date`    | optional | Deadline (`YYYY-MM-DD`)                        |
| `category`    | optional | `work`, `study`, `health`, `hobby`              |
| `status`      | optional | `new`, `in_progress`, `done`, `deleted`         |
| `parent_id`   | optional | Id of a parent task, for subtasks               |

## Project Structure

```
src/aurora/
├── cli.py             # CLI commands (Typer)
├── main.py            # FastAPI app entrypoint
├── routes/
│   └── tasks.py        # /tasks REST endpoints
├── schemas.py          # Pydantic request/response schemas
├── crud.py             # Create, read, update, delete operations
├── storage/
│   ├── protocol.py     # Storage interface (Protocol)
│   ├── sqlite_storage.py # SQLite implementation
│   └── json_storage.py   # JSON implementation
├── task.py             # Data model (Pydantic BaseModel + enums)
├── config.py           # Paths and settings
└── exceptions.py       # Custom exceptions
tests/
└── crud_test.py        # Automated tests
```

## Running Tests

```bash
uv run pytest tests/
```

## Roadmap

- [x] CLI (Typer + Rich)
- [x] REST API (FastAPI)
- [ ] Web frontend (React) — in progress on a dedicated branch

## License

MIT