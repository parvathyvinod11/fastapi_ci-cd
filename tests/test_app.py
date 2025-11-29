from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_tasks():
    res = client.get("/tasks")
    assert res.status_code == 200
    assert "tasks" in res.json()

def test_add_task():
    res = client.post("/tasks", json={"name": "Buy milk"})
    assert res.status_code == 200

def test_delete_task():
    client.post("/tasks", json={"name": "Temp Task"})
    res = client.delete("/tasks/0")
    assert res.status_code == 200
    assert res.json()["message"] == "Task deleted!"
