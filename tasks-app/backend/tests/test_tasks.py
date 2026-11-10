"""Task routes: each user sees and changes only their own tasks."""

from uuid import uuid4

from fastapi.testclient import TestClient


def create(client: TestClient, title: str) -> dict:
    response = client.post("/api/tasks", json={"title": title})
    assert response.status_code == 201, response.text
    return response.json()


def test_create_and_list_tasks(alice: TestClient) -> None:
    create(alice, "Buy milk")
    create(alice, "  Write the report  ")

    titles = [task["title"] for task in alice.get("/api/tasks").json()]

    assert titles == ["Buy milk", "Write the report"]


def test_mark_a_task_done_and_rename_it(alice: TestClient) -> None:
    task = create(alice, "Buy milk")

    response = alice.patch(f"/api/tasks/{task['id']}", json={"done": True, "title": "Buy oat milk"})

    assert response.status_code == 200
    assert response.json()["done"] is True
    assert response.json()["title"] == "Buy oat milk"


def test_delete_a_task(alice: TestClient) -> None:
    task = create(alice, "Buy milk")

    assert alice.delete(f"/api/tasks/{task['id']}").status_code == 204
    assert alice.get("/api/tasks").json() == []


def test_empty_or_long_title_is_rejected(alice: TestClient) -> None:
    assert alice.post("/api/tasks", json={"title": ""}).status_code == 422
    assert alice.post("/api/tasks", json={"title": "x" * 201}).status_code == 422


def test_whitespace_only_title_is_rejected(alice: TestClient) -> None:
    task = create(alice, "Buy milk")

    assert alice.post("/api/tasks", json={"title": "   "}).status_code == 422
    assert alice.patch(f"/api/tasks/{task['id']}", json={"title": "   "}).status_code == 422
    assert alice.get("/api/tasks").json()[0]["title"] == "Buy milk"


def test_tasks_need_a_session(client: TestClient) -> None:
    task_id = uuid4()

    assert client.get("/api/tasks").status_code == 401
    assert client.post("/api/tasks", json={"title": "Buy milk"}).status_code == 401
    assert client.patch(f"/api/tasks/{task_id}", json={"done": True}).status_code == 401
    assert client.delete(f"/api/tasks/{task_id}").status_code == 401


def test_users_do_not_see_each_others_tasks(alice: TestClient, bob: TestClient) -> None:
    create(alice, "Alice's task")

    assert bob.get("/api/tasks").json() == []


def test_users_cannot_change_or_delete_each_others_tasks(
    alice: TestClient, bob: TestClient
) -> None:
    task = create(alice, "Alice's task")

    assert bob.patch(f"/api/tasks/{task['id']}", json={"done": True}).status_code == 404
    assert bob.delete(f"/api/tasks/{task['id']}").status_code == 404
    assert alice.get("/api/tasks").json()[0]["done"] is False


def test_unknown_task_is_not_found(alice: TestClient) -> None:
    assert alice.patch(f"/api/tasks/{uuid4()}", json={"done": True}).status_code == 404
