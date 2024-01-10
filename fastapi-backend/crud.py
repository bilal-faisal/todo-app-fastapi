from fastapi import FastAPI, Body, Header, HTTPException, Depends

app : FastAPI = FastAPI()

# Welcome message
@app.get("/")
def welcome() -> dict:
    return {"message" : "Welcome to Todo API"}


# Generate user_id
@app.post("/user_id")
def generate_user_id() -> dict:
    # Generate user_id and store it in database
    return {"user_id" : ""}


# Get all todos
@app.get("/todos")
def get_todos(user_id: str = Header(default=None)) -> dict:
    if user_id:
        # validate whether user_id exists in database
        exists:bool = True
        if exists:
            # get all todos on the basis of user_id
            todos : list[dict] = []
            return {"status": "success", "todos" : todos, "user_id" : user_id}
        
        return {"status": "error", "message" : "Invalid user_id"}
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "user_id not provided"}


# Post a todo
@app.post("/todo")
def post_todo(todo:dict = Body(embed=True), user_id: str = Header(default=None)):
    if user_id:
        # Validate whether user_id exists in database
        exists:bool = True
        if exists:
            # post the todo on the basis of user_id
            return {"message" : "Todo Posted", "todo" : todo, "user_id" : user_id}
        
        return {"status": "error", "message" : "Invalid user_id"}
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "user_id not provided"}


# Delete a todo
@app.delete("/todo")
def delete_todo(todo_id:int = Body(embed=True), user_id: str = Header(default=None)):
    if user_id:
        # Validate whether user_id exists in database
        exists:bool = True
        if exists:
            # delete the todo on the basis of user_id and todo_id
            return {"message" : "Todo Deleted", "todo_id" : todo_id, "user_id" : user_id}
        
        return {"status": "error", "message" : "Invalid user_id"}
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "user_id not provided"}


# Update a todo
@app.patch("/todo")
def update_todo(todo_id:int = Body(), todo:dict = Body(), user_id: str = Header(default=None)):
    if user_id:
        # Validate whether user_id exists in database
        exists:bool = True
        if exists:
            # update the todo on the basis of user_id and todo_id
            return {"message" : "Todo Updated", "todo_id" : todo_id, "todo" : todo, "user_id" : user_id}
        
        return {"status": "error", "message" : "Invalid user_id"}
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "user_id not provided"}