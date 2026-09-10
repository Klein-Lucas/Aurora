from aurora.crud import TaskCRUD
from aurora.storage.sqlite_storage import SQLiteStorage
from aurora.routes.tasks import get_crud
from aurora.main import app
from pathlib import Path
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client(tmp_path: Path):
    def get_crud_override() -> TaskCRUD:
        storage = SQLiteStorage(path=tmp_path / "test.db")
        return TaskCRUD(storage=storage)
    
    app.dependency_overrides[get_crud] = get_crud_override
    yield TestClient(app=app)
    app.dependency_overrides.clear()

def test_api_create_task(client: TestClient):
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert "id" in data