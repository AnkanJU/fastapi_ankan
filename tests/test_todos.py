def get_auth_headers(client, email="todouser@example.com", password="password123"):
    client.post("/users/register", json={"email": email, "password": password})
    login_res = client.post("/users/login", data={"username": email, "password": password})
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_and_get_todo(client):
    headers = get_auth_headers(client)

    # Create Todo
    create_res = client.post(
        "/todos/",
        json={"title": "Buy Grocery Items", "description": "Milk and Eggs"},
        headers=headers
    )
    assert create_res.status_code == 201
    todo_id = create_res.json()["id"]

    # Retrieve Todos
    get_res = client.get("/todos/", headers=headers)
    assert get_res.status_code == 200
    todos = get_res.json()
    assert len(todos) == 1
    assert todos[0]["title"] == "Buy Grocery Items"

def test_unauthorized_todo_access(client):
    response = client.get("/todos/")
    assert response.status_code == 401