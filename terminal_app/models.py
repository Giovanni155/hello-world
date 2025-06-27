from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import sqlite3

from .db import get_connection, initialize_db


def _dict_from_row(row: sqlite3.Row):
    return {k: row[k] for k in row.keys()}


def create_category(name: str) -> int:
    if not name:
        raise ValueError("Category name is required")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO categories(name) VALUES(?)", (name,))
    conn.commit()
    category_id = cur.lastrowid
    conn.close()
    return category_id


def list_categories() -> List[dict]:
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM categories ORDER BY id").fetchall()
    conn.close()
    return [_dict_from_row(r) for r in rows]


def create_task(title: str, description: str = "", category_id: Optional[int] = None, due_date: Optional[str] = None) -> int:
    if not title:
        raise ValueError("Task title is required")
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("due_date must be in YYYY-MM-DD format")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks(title, description, category_id, due_date) VALUES(?,?,?,?)",
        (title, description, category_id, due_date),
    )
    conn.commit()
    task_id = cur.lastrowid
    conn.close()
    return task_id


def list_tasks(show_completed: bool = True) -> List[dict]:
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT * FROM tasks"
    if not show_completed:
        query += " WHERE completed = 0"
    query += " ORDER BY due_date IS NULL, due_date"
    rows = cur.execute(query).fetchall()
    conn.close()
    return [_dict_from_row(r) for r in rows]


def complete_task(task_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET completed = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (task_id,),
    )
    conn.commit()
    conn.close()


# Initialize database on module import
initialize_db()
