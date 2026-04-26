import pytest
from pymongo.errors import WriteError


@pytest.mark.integration
def test_create_returns_inserted_todo(todo_dao):
    payload = {"description": "Write assignment report", "done": False}

    created = todo_dao.create(payload)

    assert created["description"] == payload["description"]
    assert created["done"] is payload["done"]
    assert "_id" in created
    assert "$oid" in created["_id"]


@pytest.mark.integration
def test_create_raises_when_required_description_is_missing(todo_dao):
    with pytest.raises(WriteError):
        todo_dao.create({"done": False})


@pytest.mark.integration
def test_create_raises_when_done_has_wrong_type(todo_dao):
    with pytest.raises(WriteError):
        todo_dao.create({"description": "Invalid done type", "done": "False"})


@pytest.mark.integration
@pytest.mark.xfail(
    reason=(
        "Seeded defect: `uniqueItems` in the validator does not enforce uniqueness "
        "for a scalar field across documents."
    ),
)
def test_create_raises_for_duplicate_description(todo_dao):
    todo_dao.create({"description": "Duplicate me", "done": False})

    with pytest.raises(WriteError):
        todo_dao.create({"description": "Duplicate me", "done": True})
