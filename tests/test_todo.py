from http import HTTPStatus

from fast_zero.models import Todo
from tests.conftest import TodoFactory


def teste_create_todo(client, token):
    response = client.post(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test todo",
            "description": "Test description",
            "state": "draft",
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos, user_id=user.id)
    )
    session.commit()

    response = client.get(
        "/todos/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_should_return_2_limit(session, client, user, token):
    expected_todos = 5
    result_todos = 2
    session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos, user_id=user.id)
    )
    session.commit()

    response = client.get(
        f"/todos/?limit={result_todos}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["todos"]) == result_todos


def test_list_todos_should_return_4_offset(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos, user_id=user.id)
    )
    session.commit()

    response = client.get(
        "/todos/?offset=1", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["todos"]) == expected_todos - 1


def test_list_todos_should_return_1_todos_title_filter(
    session, client, user, token
):
    expected_todos = 1
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos + 5, user_id=user.id, title="Not this one"
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, title="the answer is 42"
        )
    )
    session.commit()

    response = client.get(
        "/todos/?title=42", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_should_return_1_todos_description_filter(
    session, client, user, token
):
    expected_todos = 1
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos + 5, user_id=user.id, description="Not this one"
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, description="the answer is 42"
        )
    )
    session.commit()

    response = client.get(
        "/todos/?description=42", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_should_return_1_todos_state_filter(
    session, client, user, token
):
    expected_todos = 1
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos + 5, user_id=user.id, state="draft"
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, state="doing"
        )
    )
    session.commit()

    response = client.get(
        "/todos/?state=doing", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["todos"]) == expected_todos


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        f"/todos/{todo.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": "Task has been deeleted successfully"
    }


def test_delete_todo_not_found(client, token):
    response = client.delete(
        f"/todos/{10}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found"}


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f"/todos/{1}",
        json={"title": "new title"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK


def test_patch_todo_not_found(client, token):
    response = client.patch(
        f"/todos/{10}", json={}, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found"}


def test_list_todos_should_return_all_expected_fields__exercicio(
    session, client, user, token, mock_db_time
):
    with mock_db_time(model=Todo) as time:
        todo = TodoFactory.create(user_id=user.id)
        session.add(todo)
        session.commit()

    session.refresh(todo)
    response = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.json()["todos"] == [
        {
            "created_at": time.isoformat(),
            "updated_at": time.isoformat(),
            "description": todo.description,
            "id": todo.id,
            "state": todo.state,
            "title": todo.title,
        }
    ]
