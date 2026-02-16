def test_login(client):
    client.post("/api/v1/auth/register", json={
        "email": "user@test.com",
        "password": "123456"
    })

    res = client.post("/api/v1/auth/login", json={
        "email": "user@test.com",
        "password": "123456"
    })

    assert res.status_code == 200
    assert "access_token" in res.json
