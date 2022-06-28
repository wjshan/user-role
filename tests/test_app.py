def test_index(api_client):
    response = api_client.get("/version")
    assert response.status_code == 200
