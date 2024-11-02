from http import HTTPStatus


def teste_get_token(client, user):
    response = client.post(
        "auth/token",
        data={"username": user.email, "password": user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "bearer"
    assert "access_token" in token


def teste_get_token_wrong_pwd(client, user):
    response = client.post(
        "auth/token",
        data={"username": user.email, "password": "morango"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def teste_get_token_wrong_user(client, user):
    response = client.post(
        "auth/token",
        data={"username": "morango", "password": user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
