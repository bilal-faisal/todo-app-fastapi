import os
from dotenv import load_dotenv
from fastapi import FastAPI, Body, Header
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

# Create a FastAPI instance
app : FastAPI = FastAPI()


# Welcome message
@app.get("/")
def welcome() -> dict:
    return {"message" : "Welcome to Todo API"}


# Add new user 
@app.post("/user")
def generate_user_id(
        name : str = Body(default=None), 
        email : str = Body(default=None)
    ) -> dict:

    if(name is None or email is None):
        return {
            "status" : "error", 
            "message" : "Missing body parameter. Kindly provide both name and email."
        }

    with engine.connect() as conn:
        # check if email already exists
        result = conn.execute(
            text("SELECT userid FROM users WHERE email = :email"), 
            {"email": email}
        )
        user_id = result.scalar()

        if user_id:
            return {"status": "existing_user", "message": "Email already exists", "user_id": user_id}
        
        # Add new user
        result = conn.execute(
            text("INSERT INTO users (name, email) VALUES (:name, :email) RETURNING userid"), 
            {"name": name, "email": email}
        )
        conn.commit()
        user_id = result.scalar()

        return {"status": "success", "user_id": user_id}


# Get all todos
@app.get("/todos")
def get_todos(user_id: str = Header(default=None)) -> dict:
    if user_id is None:
        return {"status": "error", "message" : "user_id not provided in Header"}
    
    # validate whether user_id exists in database
    with engine.connect() as conn:
        result = conn.execute(text("SELECT EXISTS(SELECT 1 FROM users WHERE userid = :user_id)"), {"user_id": user_id})
        exists = result.scalar()
        if not exists:
            return {"status": "error", "message" : "Invalid user_id"}
    
    todos : list[dict] = []
    # get all todos on the basis of user_id
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT todoid, title, description from todos WHERE userid = {user_id}"))            
        for row in result.all():
            todos.append({
                "todo_id" : row[0],
                "title" : row[1],
                "description" : row[2]
            })
    
    return {"status": "success", "todos" : todos }


# Post a todo
@app.post("/todo")
def post_todo(
        title:str = Body(default=None), 
        description:str = Body(default=None), 
        user_id: str = Header(default=None)
    ):
    if(title is None or description is None or user_id is None):
        return {
            "status" : "error", 
            "message" : "Missing body or header parameter. Kindly provide both title and description in body and user_id in header."
        }

    # validate whether user_id exists in database
    with engine.connect() as conn:
        result = conn.execute(text("SELECT EXISTS(SELECT 1 FROM users WHERE userid = :user_id)"), {"user_id": user_id})
        exists = result.scalar()
        if not exists:
            return {"status": "error", "message" : "Invalid user_id"}
    
    # post the todo on the basis of user_id and get todo_id
    with engine.connect() as conn:
        result = conn.execute(
            text("INSERT INTO todos (userid, title, description) VALUES (:userid, :title, :description) RETURNING todoid"), 
            {"userid": user_id, "title": title, "description": description }
        )
        conn.commit()
        todo_id = result.scalar()

        return {"message" : "Todo Posted", "todo_id" : todo_id, "user_id" : user_id}


# Delete a todo
@app.delete("/todo")
def delete_todo(todo_id:int = Body(embed=True), user_id: str = Header(default=None)):
    if user_id is None or todo_id is None:
        return {"status": "error", "message" : "user_id or todo_id missing. user_id and todo_id must be provided in body and header respectively"}

    # validate whether todo_id exists in correspondance with user_id in database
    with engine.connect() as conn:
        result = conn.execute(text("SELECT EXISTS(SELECT 1 FROM todos WHERE todoid = :todo_id AND userid = :user_id)"), {"todo_id": todo_id, "user_id": user_id})
        exists = result.scalar()
        if not exists:
            return {"status": "error", "message" : "Invalid user_id or todo_id."}

    # delete the todo on the basis of user_id and todo_id
    with engine.connect() as conn:
        conn.execute(text(f"DELETE FROM todos WHERE todoid = {todo_id} AND userid = {user_id}"))
        conn.commit()

        return {"message" : "Todo Deleted", "todo_id" : todo_id, "user_id" : user_id}


# Update a todo
@app.patch("/todo")
def update_todo(
        user_id: str = Header(default=None),
        todo_id:int = Body(default=None), 
        title:str = Body(default=""), 
        description:str = Body(default="")
    ):

    if user_id is None or todo_id is None:
        return {"status": "error", "message" : "user_id or todo_id missing. user_id and todo_id must be provided in body and header respectively"}

    if title == "" and description == "":
        return {"status": "error", "message" : "Both title and description cannot be empty"}

    # validate whether todo_id exists in correspondance with user_id in database
    with engine.connect() as conn:
        result = conn.execute(text("SELECT EXISTS(SELECT 1 FROM todos WHERE todoid = :todo_id AND userid = :user_id)"), {"todo_id": todo_id, "user_id": user_id})
        exists = result.scalar()
        if not exists:
            return {"status": "error", "message" : "Invalid user_id or todo_id."}

    # update the todo on the basis of body parameters
    with engine.connect() as conn:
        if title != "" and description != "":
            conn.execute(text(f"UPDATE todos SET title = '{title}', description = '{description}' WHERE todoid = {todo_id} AND userid = {user_id}"))
        elif title != "":
            conn.execute(text(f"UPDATE todos SET title = '{title}' WHERE todoid = {todo_id} AND userid = {user_id}"))
        elif description != "":
            conn.execute(text(f"UPDATE todos SET description = '{description}' WHERE todoid = {todo_id} AND userid = {user_id}"))
            
        conn.commit()

    return {"message" : "Todo Updated", "todo_id" : todo_id}