def test_register_returns_token(client):
    """Регистрация без токена возвращает 201 и токен."""
    response = client.post(
        "/api/auth/register/",
        {"username": "newuser", "password": "StrongPass12345"},
        format="json",
    )
    assert response.status_code == 201
    assert "token" in response.json()


def test_login_returns_token(client, user):
    """Вход существующего пользователя возвращает 200 и токен."""
    response = client.post(
        "/api/auth/login/",
        {"username": "alice", "password": "StrongPass12345"},
        format="json",
    )
    assert response.status_code == 200
    assert "token" in response.json()


def test_login_wrong_password(client, user):
    """Неверный пароль возвращает 400."""
    response = client.post(
        "/api/auth/login/", {"username": "alice", "password": "wrong"}, format="json"
    )
    assert response.status_code == 400
