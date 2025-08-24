from operations import add_user
from models import User


def test_add_user_into_db(session):
    user = add_user(
        session=session,
        username="sheldoncooper",
        password="difficultpassword",
        email="sheldon@example.com",
    )
    assert (
        session.query(User)
        .filter(User.id == user.id)
        .first()
        == user
    )
