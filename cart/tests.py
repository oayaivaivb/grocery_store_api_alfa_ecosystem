from decimal import Decimal


def add_item(client, quantity=2):
    """Вспомогательная функция: добавляет продукт в корзину с указанным количеством."""
    return client.post(
        "/api/cart/items/",
        {"product_slug": "syr-gauda", "quantity": quantity},
        format="json",
    )


def test_cart_requires_auth(client):
    """Доступ к корзине без токена — 401."""
    assert client.get("/api/cart/").status_code == 401
    assert add_item(client).status_code == 401


def test_add_item_to_cart(auth_client, create_product):
    """Добавление нового продукта в корзину возвращает 201."""
    create_product()
    response = add_item(auth_client, 2)
    assert response.status_code == 201
    assert response.json()["quantity"] == 2


def test_add_same_product_increases_quantity(auth_client, create_product):
    """Повторное добавление одного продукта суммирует количество и возвращает 200."""
    create_product()
    add_item(auth_client, 2)
    response = add_item(auth_client, 3)
    assert response.status_code == 200
    assert response.json()["quantity"] == 5


def test_add_unknown_product(auth_client):
    """Добавление несуществующего продукта возвращает 400."""
    response = auth_client.post(
        "/api/cart/items/", {"product_slug": "net-takogo"}, format="json"
    )
    assert response.status_code == 400


def test_cart_totals(auth_client, create_product):
    """Проверяет правильность total_quantity и total_price."""
    create_product()
    add_item(auth_client, 2)
    data = auth_client.get("/api/cart/").json()
    assert data["total_quantity"] == 2
    assert Decimal(str(data["total_price"])) == Decimal("900.00")


def test_update_and_delete_item(auth_client, create_product):
    """PATCH изменяет количество, DELETE удаляет позицию (204)."""
    create_product()
    item_id = add_item(auth_client, 1).json()["id"]
    response = auth_client.patch(
        f"/api/cart/items/{item_id}/", {"quantity": 5}, format="json"
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 5
    assert auth_client.delete(f"/api/cart/items/{item_id}/").status_code == 204


def test_clear_cart(auth_client, create_product):
    """DELETE /cart/ очищает все позиции."""
    create_product()
    add_item(auth_client, 2)
    assert auth_client.delete("/api/cart/").status_code == 204
    assert auth_client.get("/api/cart/").json()["total_quantity"] == 0


def test_cannot_touch_other_users_item(auth_client, other_client, create_product):
    """Пользователь не может изменить или удалить позицию чужой корзины — 404."""
    create_product()
    item_id = add_item(auth_client, 1).json()["id"]
    response = other_client.patch(
        f"/api/cart/items/{item_id}/", {"quantity": 9}, format="json"
    )
    assert response.status_code == 404
    assert other_client.delete(f"/api/cart/items/{item_id}/").status_code == 404
