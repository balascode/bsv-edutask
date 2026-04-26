import pytest
from unittest.mock import MagicMock, patch

from src.controllers.usercontroller import UserController


@pytest.fixture
def mocked_dao():
    return MagicMock()


@pytest.fixture
def sut(mocked_dao):
    return UserController(dao=mocked_dao)


@pytest.mark.unit
def test_get_user_by_email_raises_for_invalid_email(sut, mocked_dao):
    with pytest.raises(ValueError, match="invalid email address"):
        sut.get_user_by_email("not-an-email")

    mocked_dao.find.assert_not_called()


@pytest.mark.unit
def test_get_user_by_email_returns_single_user(sut, mocked_dao):
    user = {"firstName": "Jane", "lastName": "Doe", "email": "jane@doe.com"}
    mocked_dao.find.return_value = [user]

    result = sut.get_user_by_email("jane@doe.com")

    assert result == user
    mocked_dao.find.assert_called_once_with({"email": "jane@doe.com"})


@pytest.mark.unit
def test_get_user_by_email_returns_first_user_and_warns_for_duplicates(sut, mocked_dao):
    users = [
        {"firstName": "Jane", "lastName": "Doe", "email": "jane@doe.com"},
        {"firstName": "Janet", "lastName": "Doe", "email": "jane@doe.com"},
    ]
    mocked_dao.find.return_value = users

    with patch("builtins.print") as mocked_print:
        result = sut.get_user_by_email("jane@doe.com")

    assert result == users[0]
    mocked_dao.find.assert_called_once_with({"email": "jane@doe.com"})
    mocked_print.assert_called_once_with(
        "Error: more than one user found with mail jane@doe.com"
    )


@pytest.mark.unit
def test_get_user_by_email_returns_none_when_no_user_exists(sut, mocked_dao):
    mocked_dao.find.return_value = []

    result = sut.get_user_by_email("jane@doe.com")

    assert result is None
    mocked_dao.find.assert_called_once_with({"email": "jane@doe.com"})


@pytest.mark.unit
def test_get_user_by_email_propagates_dao_errors(sut, mocked_dao):
    mocked_dao.find.side_effect = RuntimeError("database is down")

    with pytest.raises(RuntimeError, match="database is down"):
        sut.get_user_by_email("jane@doe.com")
