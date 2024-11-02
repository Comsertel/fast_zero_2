from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testeusername",
            "email": "test@teste.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "testeusername",
        "email": "test@teste.com",
        "id": 1,
    }


def test_read_empty_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.json() == {"users": [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def teste_creat_user_username_already_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "Teste",
            "email": "emailnovo@ig.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username already exists"}


def teste_creat_user_email_already_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "Novo",
            "email": "teste@test.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email already exists"}


def test_delete_user_not_found(client, token):
    response = client.delete(
        "/users/666", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_user_not_found(client, token):
    response = client.put(
        "/users/666",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}


def test_get_user_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_user_id_not_found(client):
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_other_user(client, user, token):
    response = client.delete(
        f"/users/{user.id + 1}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}
