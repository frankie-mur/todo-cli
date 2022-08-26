"""This module provides the RP To-Do CLI."""
# todo/cli.py
from turtle import bgcolor
import typer
import time
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from model import Todo
from database import get_all_todos, delete_todo, update_todo, complete_todo, insert_todo
APP_NAME = 'todo'
VERSION = '0.1.0'


app = typer.Typer()
console = Console()


@app.command(short_help='Adds an item')
def add(task: str, category: str):
    """Adds an item to the to-do list.
    """
    typer.echo(f'adding "{task}" to "{category}"')
    todo = Todo(task, category)
    insert_todo(todo)
    show()


@app.command(short_help='Deletes an item')
def delete(position: int):
    """Deletes an item from the to-do list.
    """
    typer.echo(f'deleting item at position {position}')
    # we start db at position 0, UI starts at 1
    delete_todo(position-1)
    show()


@app.command(short_help='Updates an item')
def update(position: int, task: str = None, category: str = None):
    """Updates an item in the to-do list.
    """
    typer.echo(f'updating item at position {position}')
    update_todo(position-1, task, category)
    show()


@app.command(short_help="Marks an item as complete")
def complete(position: int):
    typer.echo(f'complete item at position {position}')
    complete_todo(position-1)
    show()


@app.command(short_help="Starts a 25min podoromo timer")
def pomo(duration: int):
    with Progress() as progress:
        duration = duration * 60
        task = progress.add_task("[red] 🍅 Pomodoro", total=duration)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)

    typer.echo("🍅 Time's up!")


@ app.command(short_help='Lists all items as table')
def ls():
    """Lists all items in the to-do list.
    """
    tasks = get_all_todos()

    table = Table(title="[bold blue]Todo[/bold blue]")
    table.add_column("#", style="dim", width=3,
                     justify="right", no_wrap=True)
    table.add_column("Tasks", min_width=20, style="magenta")
    table.add_column("Category", min_width=12, justify="right", style="cyan")
    table.add_column("Done", min_width=6, justify="right")

    def get_categorty_colors(category: str) -> str:
        COLORS = {'Learning': 'green', 'Work': 'blue',
                  'Home': 'red', 'Study': 'yellow', 'Sports': 'magenta', "Code": "cyan"}
        if category in COLORS:
            return COLORS[category]

        return 'white'

    for idx, task in enumerate(tasks, start=1):
        color = get_categorty_colors(task.category)
        is_done = '✅' if task.status == 2 else '❌'

        table.add_row(str(idx), task.task,
                      f'[{color}]{task.category}[/{color}]', is_done)

    console.print(table)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{APP_NAME} {VERSION}")
        raise typer.Exit()


@ app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version and exit",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    return


def main():
    app(prog_name=f'{APP_NAME}')


if __name__ == "__main__":
    main()
