""" Tests methods for User """

from qiboconnection.models.user import User


def test_user_constructor():
    """Test User class constructor."""
    user = User(user_id=1, username="test-user", api_key="000-3333")
    assert isinstance(user, User)
    print(user.__dict__)
    assert user.user_id == 1
    assert user.username == "test-user"
    assert user.api_key == "000-3333"
