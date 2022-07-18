import sqlite3
from typing import List
import datetime
from model import Todo

conn = sqlite3.connect('todos.db')
c = conn.cursor()


def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS todos(
        task text,  
        category text,
        date_added text,
        data_completed text,
        status integer,
        position integer
    )""")


create_table()


def insert_todo(todo: Todo):
    c.execute('select count(*) from todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        c.execute('INSERT into todos VALUES (:task, :category, :date_added, :data_completed, :status, :position)',
                  {'task': todo.task, 'category': todo.category, 'date_added': todo.date_added, 'data_completed': todo.data_completed, 'status': todo.status, 'position': todo.position})


def get_all_todos() -> List[Todo]:
    c.execute('select * from todos')
    todos = c.fetchall()
    return [Todo(task=todo[0], category=todo[1], date_added=todo[2], data_completed=todo[3], status=todo[4], position=todo[5]) for todo in todos]


def delete_todo(position):
    c.execute('SELECT count(*) from todos')
    count = c.fetchone()[0]
    with conn:
        c.execute('DELETE from todos where position = :position',
                  {'position': position})
        for pos in range(position, count):
            change_position(pos, pos-1, False)


def change_position(old_position: int, new_position: int, commit: bool = True):
    c.execute('UPDATE todos SET position = :position_new WHERE position = :position_old',
              {"position_new": new_position, "position_old": old_position})
    if commit:
        conn.commit()


def update_todo(position: int, task: str, category: str):
    with conn:
        if task is not None and category is not None:
            c.execute('UPDATE todos SET task = :task, category = :category WHERE position = :position',
                      {'task': task, 'category': category, 'position': position})
        elif task is not None:
            c.execute('UPDATE todos SET task = :task WHERE position = :position',
                      {'task': task, 'position': position})
        elif category is not None:
            c.execute('UPDATE todos SET category = :category WHERE position = :position',
                      {'category': category, 'position': position})


def complete_todo(position: int):
    with conn:
        c.execute('UPDATE todos SET status = 2, data_completed = :data_completed WHERE position = :position',
                  {'data_completed': datetime.datetime.now().isoformat(), 'position': position})
