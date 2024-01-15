from fastapi.testclient import TestClient
from app.crud import app
from random import randint

client = TestClient(app)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def test_base_route():
    res = client.get('/')
    assert res.status_code == 200
    assert res.json() == {'message': 'Welcome to Todo API'}

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