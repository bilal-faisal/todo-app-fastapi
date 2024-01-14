import data
from fastapi import FastAPI, Body, Header

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
        name : str = Body(default=None), 
        email : str = Body(default=None)
    ) -> dict:

    if(name is None or email is None):
        return {
            "status" : "error", 
            "message" : "Missing body parameter. Kindly provide both name and email."
        }

    # check if email already exists
    user_id = data.get_userid_from_email(email)
    if user_id:
        return {"status": "existing_user", "message": "Email already exists", "user_id": user_id}
    
    # add new user
    new_user_id = data.add_user(name, email)
    return {"status": "success", "user_id": new_user_id}

# Get single todo
@app.get("/todo/{todo_id}")
def get_todo(todo_id: int, user_id: str = Header(default=None)) -> dict:
    if user_id is None:
        return {"status": "error", "message" : "user_id not provided in Header"}
    
    # validate whether user_id exists in database
    exists = data.check_user_exists(user_id)
    if not exists:
        return {"status": "error", "message" : "Invalid user_id"}

    # get todo on the basis of todo_id and user_id
    todo = data.get_single_todo(todo_id, user_id)
    if todo is None:
        return {"status": "error", "message" : "Todo not found"}
    
    return {"status": "success", "todo" : todo}

# Get all todos
@app.get("/todos")
def get_todos(user_id: str = Header(default=None)) -> dict:
    if user_id is None:
        return {"status": "error", "message" : "user_id not provided in Header"}
    
    # validate whether user_id exists in database
    exists = data.check_user_exists(user_id)
    if not exists:
        return {"status": "error", "message" : "Invalid user_id"}

    # get all todos on the basis of user_id
    todos : list[dict] = data.get_all_todos(user_id)

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
    exists = data.check_user_exists(user_id)
    if not exists:
        return {"status": "error", "message" : "Invalid user_id"}

    # post the todo on the basis of user_id and get todo_id
    todo_id = data.add_todo(user_id, title, description)
    return {"message" : "Todo Posted", "todo_id" : todo_id, "user_id" : user_id}

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
    exists = data.check_todo_exists(todo_id, user_id)
    if not exists:
        return {"status": "error", "message" : "Invalid user_id or todo_id."}
    
    # update the todo on the basis of body parameters
    data.update_todo(user_id, todo_id, title, description)

    return {"message" : "Todo Updated", "todo_id" : todo_id}

# Delete a todo
@app.delete("/todo")
def delete_todo(todo_id:int = Body(embed=True), user_id: str = Header(default=None)):
    if user_id is None or todo_id is None:
        return {"status": "error", "message" : "user_id or todo_id missing. user_id and todo_id must be provided in body and header respectively"}

    # validate whether todo_id exists in correspondance with user_id in database
    exists = data.check_todo_exists(todo_id, user_id)
    if not exists:
        return {"status": "error", "message" : "Invalid user_id or todo_id."}
    
    # delete the todo on the basis of user_id and todo_id
    data.delete_todo(todo_id, user_id)

    return {"message" : "Todo Deleted", "todo_id" : todo_id, "user_id" : user_id}

# start uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("crud:app", reload=True)