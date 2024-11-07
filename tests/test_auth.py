from http import HTTPStatus

from freezegun import freeze_time


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


def test_token_expired_after_time(client, user):
    with freeze_time("2023-11-05 13:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.email, "password": user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]
        assert token

    with freeze_time("2023-11-05 13:31:00"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "newname",
                "email": "new@email.com",
                "password": "wrong",
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}


def test_token_wrong_password(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": "wrong"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_token_wrong_user(client, user):
    response = client.post(
        "/auth/token",
        data={
            "username": "doido@gmail.com.br",
            "password": user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}
