def test_register_user(client):
    response = client.post(
        "/users/register",
        json={"email": "testuser@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

def test_login_user(client):
    # Register user first
    client.post(
        "/users/register",
        json={"email": "loginuser@example.com", "password": "password123"}
    )

    # Attempt login
    response = client.post(
        "/users/login",
        data={"username": "loginuser@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"