# I'll be writing test code here using pytest

from fastapi.testclient import TestClient
from app.crud import app

client = TestClient(app)

def test_base_route():
    res = client.get('/')
    assert res.status_code == 200
    assert res.json() == {'message': 'Welcome to Todo API'}