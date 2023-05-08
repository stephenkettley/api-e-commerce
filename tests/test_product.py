def test_get_all_products(authorized_client: callable) -> None:
    """Tests the route to get all products."""
    response = authorized_client.get("/product/all")
    assert response.status_code == 200
