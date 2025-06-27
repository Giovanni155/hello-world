from typing import Optional
import os
import sys

if __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from terminal_app import models
else:
    from . import models


def print_categories():
    cats = models.list_categories()
    if not cats:
        print("No categories found.")
    for c in cats:
        print(f"{c['id']}: {c['name']}")


def print_tasks(show_completed: bool = True):
    tasks = models.list_tasks(show_completed=show_completed)
    if not tasks:
        print("No tasks found.")
    for t in tasks:
        status = 'X' if t['completed'] else ' '
        due = t['due_date'] or '-'
        print(f"[{status}] {t['id']} {t['title']} (due: {due})")


def add_category():
    name = input("Category name: ").strip()
    try:
        models.create_category(name)
        print("Category added.")
    except Exception as e:
        print(f"Error: {e}")


def add_task():
    title = input("Title: ").strip()
    description = input("Description: ").strip()
    cat_input = input("Category id (optional): ").strip()
    cat_id: Optional[int] = int(cat_input) if cat_input else None
    due_date = input("Due date (YYYY-MM-DD, optional): ").strip()
    if not due_date:
        due_date = None
    try:
        models.create_task(title, description, cat_id, due_date)
        print("Task added.")
    except Exception as e:
        print(f"Error: {e}")


def complete_task():
    task_id = input("Task id: ").strip()
    try:
        models.complete_task(int(task_id))
        print("Task marked as completed.")
    except Exception as e:
        print(f"Error: {e}")


def menu():
    while True:
        print("\n1. List tasks")
        print("2. Add task")
        print("3. Complete task")
        print("4. List categories")
        print("5. Add category")
        print("0. Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            print_tasks(show_completed=True)
        elif choice == "2":
            add_task()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            print_categories()
        elif choice == "5":
            add_category()
        elif choice == "0":
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    menu()
