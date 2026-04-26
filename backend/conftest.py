import os
from pathlib import Path

import pytest
import pymongo

from src.util.dao import DAO


BACKEND_DIR = Path(__file__).resolve().parent


@pytest.fixture(scope="session")
def mongo_test_url() -> str:
    """Return the MongoDB URL used only for integration tests."""
    return os.environ.get("MONGO_TEST_URL", "mongodb://localhost:27018")


@pytest.fixture(scope="session")
def mongo_client(mongo_test_url: str):
    """Create a client for the integration test MongoDB instance."""
    client = pymongo.MongoClient(mongo_test_url, serverSelectionTimeoutMS=3000)

    try:
        client.admin.command("ping")
    except Exception as exc:
        pytest.skip(
            f"MongoDB integration instance is unreachable at {mongo_test_url}: {exc}"
        )

    yield client
    client.close()


@pytest.fixture
def todo_dao(
    monkeypatch: pytest.MonkeyPatch, mongo_client, mongo_test_url: str
) -> DAO:
    """
    Provide an isolated DAO for the todo collection.

    The fixture uses a dedicated Mongo URL and drops the collection before and after
    each test so production-like data is not touched.
    """
    monkeypatch.setenv("MONGO_URL", mongo_test_url)

    previous_cwd = Path.cwd()
    os.chdir(BACKEND_DIR)

    database = mongo_client.edutask
    database.drop_collection("todo")

    try:
        dao = DAO(collection_name="todo")
        yield dao
    finally:
        database.drop_collection("todo")
        os.chdir(previous_cwd)
