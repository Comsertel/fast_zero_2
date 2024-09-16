from http import HTTPStatus


def test_root_deve_retornar_ok_e_hello_world(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}


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


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {"id": 1, "username": "testeusername", "email": "test@teste.com"}
        ]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "string2",
            "email": "user@example.com",
            "password": "string2",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "string2",
        "email": "user@example.com",
        "id": 1,
    }


def test_update_not_found(client):
    pass


def test_delete(client):
    pass
