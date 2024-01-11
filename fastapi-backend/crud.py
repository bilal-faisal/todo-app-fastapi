from fastapi import FastAPI, Body, Header
import random

app : FastAPI = FastAPI()

# Welcome message
@app.get("/")
def welcome() -> dict:
    return {"message" : "Welcome to Todo API"}


# Generate user_id
@app.post("/user_id")
def get_user_id(
        name:str = Body(default=None), 
        email:str = Body(default=None)
    ) -> dict:

    if(name is not None and email is not None):
        # TODO: check if email already exists by getting user_id
        user_id : str | None = None

        # if exists, return user_id
        if user_id is None:
            return {"status" : "existing_user", "message" : "Email already exists", "user_id": user_id}

        # TODO: if not exists, insert name and email and return user_id
        user_id = ""

        return {"user_id" : user_id}
    
    else:
        return {"status" : "error", "message" : "Missing body parameter. Kindly provide both name and email."}


# Get all todos
@app.get("/todos")
def get_todos(user_id: str = Header(default=None)) -> dict:
    if user_id:
        # TODO: validate whether user_id exists in database
        exists : bool = True

        if not exists:
            return {"status": "error", "message" : "Invalid user_id"}
        
        # TODO: get all todos on the basis of user_id
        todos : list[dict] = []
        return {"status": "success", "todos" : todos, "user_id" : user_id}
        
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "user_id not provided in Header"}


# Post a todo
@app.post("/todo")
def post_todo(
        todo:dict = Body(embed=True), 
        user_id: str = Header(default=None)
    ):
    if user_id:
        # TODO: Validate whether user_id exists in database
        exists:bool = True

        if not exists:
            return {"status": "error", "message" : "Invalid user_id"}

        # TODO: post the todo on the basis of user_id and get todo_id
        todo_id = ""
        return {"message" : "Todo Posted", "todo_id" : todo_id, "user_id" : user_id}
        
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "user_id not provided"}


# Delete a todo
@app.delete("/todo")
def delete_todo(todo_id:int = Body(embed=True), user_id: str = Header(default=None)):
    if user_id:
        # TODO: Validate whether user_id exists in database
        exists : bool = True

        if not exists:
            return {"status": "error", "message" : "Invalid user_id"}

        # TODO: delete the todo on the basis of user_id and todo_id
        return {"message" : "Todo Deleted", "todo_id" : todo_id, "user_id" : user_id}
        
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "user_id not provided"}


# Update a todo
@app.patch("/todo")
def update_todo(todo_id:int = Body(), todo:dict = Body(), user_id: str = Header(default=None)):
    if user_id:
        # TODO: Validate whether user_id exists in database
        exists:bool = True

        if not exists:
            return {"status": "error", "message" : "Invalid user_id"} 
        
        # TODO: update the todo on the basis of user_id and todo_id
        return {"message" : "Todo Updated", "todo_id" : todo_id, "todo" : todo, "user_id" : user_id}
    
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "user_id not provided"}