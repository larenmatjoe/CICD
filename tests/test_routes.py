import pytest

from app import create_app
from app.routes import _users, _user_id_counter


@pytest.fixture
def app():
    app = create_app("testing")
    return app


@pytest.fixture(autouse=True)
def reset_users():
    """Reset the in-memory user list and ID counter before and after each test."""
    _users.clear()
    _user_id_counter[0] = 0
    yield
    _users.clear()
    _user_id_counter[0] = 0


class TestIndex:
    def test_index_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_returns_welcome_message(self, client):
        response = client.get("/")
        data = response.get_json()
        assert data["message"] == "Welcome to the Flask web server!"


class TestHealth:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_ok_status(self, client):
        response = client.get("/health")
        data = response.get_json()
        assert data["status"] == "ok"


class TestUsers:
    def test_get_users_returns_empty_list(self, client):
        response = client.get("/users")
        assert response.status_code == 200
        data = response.get_json()
        assert data["users"] == []

    def test_create_user_returns_201(self, client):
        response = client.post("/users", json={"name": "Alice"})
        assert response.status_code == 201

    def test_create_user_returns_user_data(self, client):
        response = client.post("/users", json={"name": "Alice"})
        data = response.get_json()
        assert data["user"]["name"] == "Alice"
        assert data["user"]["id"] == 1

    def test_create_user_persists_in_list(self, client):
        client.post("/users", json={"name": "Alice"})
        response = client.get("/users")
        data = response.get_json()
        assert len(data["users"]) == 1
        assert data["users"][0]["name"] == "Alice"

    def test_create_multiple_users(self, client):
        client.post("/users", json={"name": "Alice"})
        client.post("/users", json={"name": "Bob"})
        response = client.get("/users")
        data = response.get_json()
        assert len(data["users"]) == 2
        assert data["users"][1]["name"] == "Bob"

    def test_create_user_missing_name_returns_400(self, client):
        response = client.post("/users", json={"age": 30})
        assert response.status_code == 400

    def test_create_user_missing_name_returns_error_message(self, client):
        response = client.post("/users", json={"age": 30})
        data = response.get_json()
        assert "error" in data

    def test_create_user_no_body_returns_400(self, client):
        response = client.post("/users", content_type="application/json")
        assert response.status_code == 400
