from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username="comsertel", email="teste@mail.com.br", password="senha"
    )
    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == "teste@mail.com.br")
    )
    assert result.username == "comsertel"
