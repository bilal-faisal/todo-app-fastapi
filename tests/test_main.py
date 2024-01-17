from fastapi.testclient import TestClient
from app.crud import app
from random import randint

client = TestClient(app)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# GET/

def test_base_route():
    res = client.get('/')
    assert res.status_code == 200
    assert res.json() == {'message': 'Welcome to Todo API'}

# POST/user

def test_add_new_user_success():
    response = client.post("/user", json={"name": "Test User", "email": f"{random_with_N_digits(10)}@test.com"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "user_id" in response.json()

def test_add_existing_user():
    response = client.post("/user", json={"name": "Jane Doe", "email": "john.doe@example.com"})
    assert response.status_code == 200
    assert response.json()["status"] == "existing_user"
    assert "user_id" in response.json()

def test_add_new_user_missing_parameters():
    # Test with missing name and email
    response = client.post("/user", json={})
    assert response.status_code == 422

    # Test with missing email
    response = client.post("/user", json={"name": "John Doe"})
    assert response.status_code == 422

    # Test with missing name
    response = client.post("/user", json={"email": "john.doe@example.com"})
    assert response.status_code == 422

def test_add_new_user_invalid_email():
    response = client.post("/user", json={"name": "Test User", "email": "invalid_email"})
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "Invalid email"

# GET/todo/n

def test_get_single_todo_missing_parameters():
    response = client.get("/todo/4")
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"

def test_get_single_todo_invalid_user_id():
    response = client.get("/todo/4", headers={"user-id":"invalid"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"

def test_get_single_todo_user_id_not_exists():
    response = client.get("/todo/4", headers={"user-id":"10000000"})
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "User does not exists"

def test_get_single_task_success():
    response = client.get("/todo/4", headers={"user-id":"20"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "todos" in response.json()

def test_get_single_todo_id_not_exists():
    response = client.get("/todo/1000000", headers={"user-id":"20"})
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "Todo not found"

# GET/todos

def test_get_all_todos_success():
    response = client.get("/todos", headers={"user-id":"20"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "todos" in response.json()

def test_get_all_todos_invalid_user_id():
    response = client.get("/todos", headers={"user-id":"invalid"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"

def test_get_all_todos_user_id_not_exists():
    response = client.get("/todos", headers={"user-id":"10000000"})
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "User does not exists"

def test_get_all_todos_missing_user_id():
    response = client.get("/todos")
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"

# POST/todo

def test_add_new_todo_success():
    response = client.post("/todo", json={"title": "Test Todo", "description": "This is a test todo"}, headers={"user-id":"20"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "todo_id" in response.json()

def test_add_new_todo_invalid_user_id():
    response = client.post("/todo", json={"title": "Test Todo", "description": "This is a test todo"}, headers={"user-id":"invalid"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"

def test_add_new_todo_user_id_not_exists():
    response = client.post("/todo", json={"title": "Test Todo", "description": "This is a test todo"}, headers={"user-id":"10000000"})
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "User does not exists"

def test_add_new_todo_missing_parameters():
    response = client.post("/todo", json={}, headers={"user-id":"20"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"

def test_add_new_todo_missing_user_id():
    response = client.post("/todo", json={"title": "Test Todo", "description": "This is a test todo"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"

# PATCH/todo

def test_update_todo_success():
    response = client.patch("/todo", json={
        "title": "Updated Todo",
        "todo_id": 10
        }, headers={"user-id":"20"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "todo_id" in response.json()

def test_update_todo_missing_both_parameters():
    response = client.patch("/todo", json={"todo_id": 10}, headers={"user-id":"20"})
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "Both title and description cannot be empty"

def test_update_todo_todo_id_not_exists():
    response = client.patch("/todo", json={"title": "Updated Todo"}, headers={"user-id":"20"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"

def test_update_todo_user_id_not_exists():
    response = client.patch("/todo", json={"title": "Updated Todo", "todo_id": "10"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"

def test_update_todo_invalid_user_id():
    response = client.patch("/todo", json={"title": "Updated Todo", "todo_id": "10"}, headers={"user-id":"invalid"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"

def test_update_todo_invalid_todo_id():
    response = client.patch("/todo", json={"title": "Updated Todo", "todo_id": "invalid"}, headers={"user-id":"20"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"

