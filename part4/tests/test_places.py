def test_create_place(client, token):
    res = client.post(
        "/api/v1/places",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Place"}
    )
    assert res.status_code == 201


def test_unauthorized_create_place(client):
    res = client.post("/api/v1/places", json={"name": "Fail"})
    assert res.status_code == 401
