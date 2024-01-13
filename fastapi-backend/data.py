import os
from typing import Any
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Engine

# Load environment variables from .env file
load_dotenv()

# Now retrieving the NEON_CONNECTION_STRING
conn_str = os.getenv("NEON_CONNECTION_STRING")

# Check if NEON_CONNECTION_STRING is set
if conn_str is None:
    print("NEON_CONNECTION_STRING environment variable is not set.")
    raise Exception("NEON_CONNECTION_STRING environment variable is not set.")

# Create a SQLAlchemy engine using the NEON_CONNECTION_STRING
engine: Engine = create_engine(conn_str)

def create_tables_if_not_exists():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                userid SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS todos (
                todoid SERIAL PRIMARY KEY,
                userid INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY (userid) REFERENCES users(userid)
            )
        """))
        conn.commit()

def get_userid_from_email(email: str) -> int | None:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT userid FROM users WHERE email = :email"),
            {"email": email}
        )
        return result.scalar()

def add_user(name: str, email: str) -> int | None:
    with engine.connect() as conn:
        result = conn.execute(
            text("INSERT INTO users (name, email) VALUES (:name, :email) RETURNING userid"),
            {"name": name, "email": email}
        )
        conn.commit()
        return result.scalar()

def check_user_exists(user_id: str) -> Any | None:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT EXISTS(SELECT 1 FROM users WHERE userid = :user_id)"),
            {"user_id": user_id}
        )
        return result.scalar()

def get_single_todo(todo_id: int, user_id: str) -> dict | None:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT todoid, title, description FROM todos WHERE todoid = :todo_id AND userid = :user_id"),
            {"todo_id": todo_id, "user_id": user_id}
        )
        todo = result.fetchone()
        if todo:
            return {
                "todo_id": todo[0],
                "title": todo[1],
                "description": todo[2]
            }
        else:
            return None

def get_all_todos(user_id: str) -> list[dict]:
    todos = []
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT todoid, title, description FROM todos WHERE userid = :user_id"),
            {"user_id": user_id}
        )
        for row in result.all():
            todos.append({
                "todo_id": row[0],
                "title": row[1],
                "description": row[2]
            })
    return todos

def add_todo(user_id: str, title: str, description: str) -> int | None:
    with engine.connect() as conn:
        result = conn.execute(
            text("INSERT INTO todos (userid, title, description) VALUES (:userid, :title, :description) RETURNING todoid"),
            {"userid": user_id, "title": title, "description": description}
        )
        conn.commit()
        return result.scalar()

def check_todo_exists(todo_id: int, user_id: str) -> bool | None:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT EXISTS(SELECT 1 FROM todos WHERE todoid = :todo_id AND userid = :user_id)"),
            {"todo_id": todo_id, "user_id": user_id}
        )
        return result.scalar()

def delete_todo(todo_id: int, user_id: str) -> None:
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM todos WHERE todoid = :todo_id AND userid = :user_id"),
            {"todo_id": todo_id, "user_id": user_id}
        )
        conn.commit()

def update_todo(user_id: str, todo_id: int, title: str, description: str) -> None:
    with engine.connect() as conn:
        if title != "" and description != "":
            conn.execute(text(f"UPDATE todos SET title = '{title}', description = '{description}' WHERE todoid = {todo_id} AND userid = {user_id}"))
        elif title != "":
            conn.execute(text(f"UPDATE todos SET title = '{title}' WHERE todoid = {todo_id} AND userid = {user_id}"))
        elif description != "":
            conn.execute(text(f"UPDATE todos SET description = '{description}' WHERE todoid = {todo_id} AND userid = {user_id}"))
            
        conn.commit()
