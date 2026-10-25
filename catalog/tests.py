def test_categories_list_has_subcategories_and_pagination(client, create_product):
    """Проверяет, что категории возвращаются с вложенными подкатегориями и пагинацией."""
    create_product()
    response = client.get("/api/categories/")
    assert response.status_code == 200
    for key in ("count", "next", "previous", "results"):
        assert key in response.json()
    category = response.json()["results"][0]
    assert category["slug"] == "molochnye"
    assert category["subcategories"][0]["slug"] == "syry"


def test_products_list_fields(client, create_product):
    """Проверяет структуру ответа продуктов: поля, категории и варианты изображений."""
    create_product()
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert response.json()["count"] == 1
    item = response.json()["results"][0]
    assert item["name"] == "Сыр Гауда"
    assert item["category"] == "Молочные продукты"
    assert item["subcategory"] == "Сыры"
    assert item["price"] == "450.00"
    assert set(item["images"]) == {"small", "medium", "large"}


def test_products_pagination(client, create_product):
    """Проверяет, что при 12 продуктах на странице возвращается 10 (PAGE_SIZE), а next не None."""
    for i in range(12):
        create_product(slug=f"product-{i}", name=f"Продукт {i}")
    data = client.get("/api/products/").json()
    assert data["count"] == 12
    assert len(data["results"]) == 10
    assert data["next"] is not None
