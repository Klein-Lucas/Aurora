from aurora.storage import JSONStorage
from aurora.crud import TaskCRUD
from aurora.task import Category, Status, Task
from aurora.exceptions import TaskNotFoundError
from uuid import UUID
from datetime import date
import typer
from rich.table import Table
from rich.console import Console

storage = JSONStorage()
crud = TaskCRUD(storage=storage)

app = typer.Typer()
console = Console()

@app.command()
def create(
    title: str,
    description: str = typer.Option(None),
    start_date: str = typer.Option(None),
    end_date: str = typer.Option(None),
    category: Category = typer.Option(None),
    status: Status = typer.Option(Status.NEW),
):
    parsed_start_date = date.fromisoformat(start_date) if start_date else None
    parsed_end_date = date.fromisoformat(end_date) if end_date else None
    task = Task(title=title, 
                description=description, 
                start_date=parsed_start_date,
                end_date=parsed_end_date,
                category=category,
                status=status)
    crud.create_task(task=task)

@app.command()
def show():
    tasks = crud.read_all()
    table = Table(title="Tasks")
    table.add_column("Index")
    table.add_column("Title")
    table.add_column("Status")
    for i,task in enumerate(tasks, start=1):
        table.add_row(str(i), task.title, task.status.value)
    console.print(table)

@app.command()
def delete(index: int):
    tasks = crud.read_all()
    if index < 1 or index > len(tasks):
        console.print("[red]Index not found[/red]")
        raise typer.Exit()
    try:
        crud.delete_by_id(id=tasks[index-1].id)
    except TaskNotFoundError:
        console.print("[red]Erro interno: task não encontrada no storage.[/red]")
        raise typer.Exit(code=1)   

@app.command()
def update(
    index: int,
    title: str = typer.Option(None),
    description: str = typer.Option(None),
    start_date: str = typer.Option(None),
    end_date: str = typer.Option(None),
    category: Category = typer.Option(None),
    status: Status = typer.Option(None),
):
    tasks = crud.read_all()
    if index < 1 or index > len(tasks):
        console.print("[red]Index not found[/red]")
        raise typer.Exit()
    try:
        task = crud.read_by_id(id=tasks[index-1].id)
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if start_date is not None:
            task.start_date = date.fromisoformat(start_date)
        if end_date is not None:
            task.end_date = date.fromisoformat(end_date)
        if category is not None:
            task.category = category
        if status is not None:
            task.status = status
        crud.update_task(updated_task=task)
    except TaskNotFoundError:
        console.print("[red]Erro interno: task não encontrada no storage.[/red]")
        raise typer.Exit(code=1)    

if __name__ == "__main__":
    app()