"""
Tests for todo REST API endpoints
"""

import pytest
from fastapi.testclient import TestClient


def test_create_todo(client: TestClient):
    """Test creating a new todo"""
    response = client.post(
        "/api/v1/todos",
        json={"title": "Test Todo", "description": "Test Description", "priority": "high"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert data["priority"] == "high"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_list_todos(client: TestClient):
    """Test listing todos"""
    # Create some todos
    client.post("/api/v1/todos", json={"title": "Todo 1"})
    client.post("/api/v1/todos", json={"title": "Todo 2"})
    
    # List todos
    response = client.get("/api/v1/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_todo(client: TestClient):
    """Test getting a specific todo"""
    # Create a todo
    create_response = client.post(
        "/api/v1/todos",
        json={"title": "Test Todo"}
    )
    todo_id = create_response.json()["id"]
    
    # Get the todo
    response = client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test Todo"


def test_update_todo(client: TestClient):
    """Test updating a todo"""
    # Create a todo
    create_response = client.post(
        "/api/v1/todos",
        json={"title": "Original Title"}
    )
    todo_id = create_response.json()["id"]
    
    # Update the todo
    response = client.put(
        f"/api/v1/todos/{todo_id}",
        json={"title": "Updated Title", "completed": True, "priority": "urgent"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["completed"] is True
    assert data["priority"] == "urgent"


def test_delete_todo(client: TestClient):
    """Test deleting a todo"""
    # Create a todo
    create_response = client.post(
        "/api/v1/todos",
        json={"title": "To Delete"}
    )
    todo_id = create_response.json()["id"]
    
    # Delete the todo
    response = client.delete(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 404


def test_filter_by_completed(client: TestClient):
    """Test filtering todos by completion status"""
    # Create completed and incomplete todos
    client.post("/api/v1/todos", json={"title": "Incomplete 1"})
    
    todo2 = client.post("/api/v1/todos", json={"title": "Complete 1"})
    client.put(
        f"/api/v1/todos/{todo2.json()['id']}",
        json={"completed": True}
    )
    
    # Filter by incomplete
    response = client.get("/api/v1/todos?completed=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["completed"] is False
    
    # Filter by complete
    response = client.get("/api/v1/todos?completed=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["completed"] is True


def test_create_todo_with_default_priority(client: TestClient):
    """Test creating a todo without specifying priority uses default"""
    response = client.post(
        "/api/v1/todos",
        json={"title": "Default Priority Todo"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["priority"] == "medium"  # Default priority


def test_priority_field(client: TestClient):
    """Test priority field is properly stored and retrieved"""
    # Create todos with different priorities
    priorities = ["low", "medium", "high", "urgent"]
    
    for priority in priorities:
        response = client.post(
            "/api/v1/todos",
            json={"title": f"{priority.capitalize()} Priority Todo", "priority": priority}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["priority"] == priority

