from fastapi import FastAPI, Body, Header
import data
from utils import validate_email

# Application initialization
data.create_tables_if_not_exists()

# Create a FastAPI instance
app : FastAPI = FastAPI()

# Welcome message
@app.get("/")
def welcome() -> dict:
    return {"message" : "Welcome to Todo API"}

# Add new user 
@app.post("/user")
def add_new_user(
        name : str = Body(), 
        email : str = Body()
    ) -> dict:
    # check if email is valid
    if not validate_email(email):
        return {"status": "error", "message": "Invalid email"}

    # check if email already exists
    user = data.get_user_data(email)
    if user:
        return {"status": "existing_user", "message": "Email already exists", "user_id": user["user_id"], "name": user["name"]}
    
    # add new user
    new_user_id = data.add_user(name, email)
    return {"status": "success", "user_id": new_user_id}

# Get single todo
@app.get("/todo/{todo_id}")
def get_todo(
        todo_id: int, 
        user_id: int = Header()
    ) -> dict:
    
    # validate whether user_id exists in database
    exists = data.check_user_exists(user_id)
    if not exists:
        return {"status": "error", "message" : "User does not exists"}

    # get todo on the basis of todo_id and user_id
    todo = data.get_single_todo(todo_id, user_id)
    if todo is None:
        return {"status": "error", "message" : "Todo not found"}
    
    return {"status": "success", "todos" : todo}

# Get all todos
@app.get("/todos")
def get_todos(
        user_id: int = Header()
    ) -> dict:
    
    # validate whether user_id exists in database
    exists = data.check_user_exists(user_id)
    if not exists:
        return {"status": "error", "message" : "User does not exists"}

    # get all todos on the basis of user_id
    todos : list[dict] = data.get_all_todos(user_id)

    return {"status": "success", "todos" : todos }

# Post a todo
@app.post("/todo")
def post_todo(
        title:str = Body(), 
        description:str = Body(default=None), 
        user_id: int = Header()
    ):
    # validate whether user_id exists in database
    exists = data.check_user_exists(user_id)
    if not exists:
        return {"status": "error", "message" : "User does not exists"}

    # post the todo on the basis of user_id and get todo_id
    todo_id = data.add_todo(user_id, title, description)
    return {"status":"success", "message" : "Todo Posted", "todo_id" : todo_id, "user_id" : user_id}

# Update a todo
@app.patch("/todo")
def update_todo(
        user_id: int = Header(),
        todo_id: int = Body(), 
        title: str = Body(default=None), 
        description:str = Body(default=None), 
    ):

    if title is None and description is None:
        return {"status": "error", "message" : "Both title and description cannot be empty"}

    # validate whether todo_id exists in correspondance with user_id in database
    exists = data.check_todo_exists(todo_id, user_id)
    if not exists:
        return {"status": "error", "message" : "Invalid user_id or todo_id."}
    
    # update the todo on the basis of body parameters
    data.update_todo(user_id, todo_id, title, description)

    return {"status":"success", "message" : "Todo Updated", "todo_id" : todo_id}

# Delete a todo
@app.delete("/todo/{todo_id}")
def delete_todo(
        todo_id:int, 
        user_id: int = Header()
    ):

    # validate whether todo_id exists in correspondance with user_id in database
    exists = data.check_todo_exists(todo_id, user_id)
    if not exists:
        return {"status": "error", "message" : "Invalid user_id or todo_id."}
    
    # delete the todo on the basis of user_id and todo_id
    data.delete_todo(todo_id, user_id)

    return {"status":"success" ,"message" : "Todo Deleted", "todo_id" : todo_id, "user_id" : user_id}

# start uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("crud:app", reload=True)