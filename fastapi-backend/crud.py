from fastapi import FastAPI, Body, Header, HTTPException, Depends

app : FastAPI = FastAPI()

# Welcome message
@app.get("/")
def welcome() -> dict:
    return {"message" : "Welcome to Todo API"}

# Generate token
@app.post("/token")
def generate_token() -> dict:
    # Generate token and store it in database
    return {"token" : "token"}

# Get all todos
@app.get("/todos")
def get_todos(token: str = Header(default=None)) -> dict:
    if token:
        # validate whether token exists in database
        exists:bool = False
        if exists:
            # get all todos on the basis of token
            todos : list[dict] = []
            return {"status": "success", "todos" : todos, "token" : token}
        
        return {"status": "error", "message" : "Invalid token"}
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "Token not provided"}


# Post a todo
@app.post("/todo")
def post_todo(todo:dict = Body(embed=True), token: str = Header(default=None)):
    if token:
        # Validate whether token exists in database
        exists:bool = True
        if exists:
            # post the todo on the basis of token
            return {"message" : "Todo Posted", "todo" : todo, "token" : token}
        
        return {"status": "error", "message" : "Invalid token"}
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "Token not provided"}


# Delete a todo
@app.delete("/todo")
def delete_todo(todo_id:int = Body(embed=True), token: str = Header(default=None)):
    if token:
        # Validate whether token exists in database
        exists:bool = True
        if exists:
            # delete the todo on the basis of token and todo_id
            return {"message" : "Todo Deleted", "todo_id" : todo_id, "token" : token}
        
        return {"status": "error", "message" : "Invalid token"}
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "Token not provided"}

# Update a todo
@app.patch("/todo")
def update_todo(todo_id:int = Body(), todo:dict = Body(), token: str = Header(default=None)):
    if token:
        # Validate whether token exists in database
        exists:bool = True
        if exists:
            # update the todo on the basis of token and todo_id
            return {"message" : "Todo Updated", "todo_id" : todo_id, "todo" : todo, "token" : token}
        
        return {"status": "error", "message" : "Invalid token"}
    else:
        # if not exists, return error message
        return {"status": "error", "message" : "Token not provided"}