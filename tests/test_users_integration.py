def test_register_and_login_user(client):
    payload = {
        "email": "testuser@example.com",
        "password": "secret123"
    }

    # Register
    r = client.post("/users/register", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == payload["email"]
    assert "id" in data

    # Duplicate register should fail
    r_dup = client.post("/users/register", json=payload)
    assert r_dup.status_code == 400

    # Login success
    r_login = client.post("/users/login", json=payload)
    assert r_login.status_code == 200
    data_login = r_login.json()
    assert data_login["email"] == payload["email"]

    # Login failure
    r_bad = client.post(
        "/users/login",
        json={"email": payload["email"], "password": "wrongpassword"},
    )
    assert r_bad.status_code == 401
