import pytest
from src.util.helpers import hasAttribute

@pytest.fixture
def obj():
    return {"clg" : "BTH"}

@pytest.mark.unit
def test_hasAttribute_True():
    assert hasAttribute(obj, "clg") == True

@pytest.mark.unit
def test_hasAttribute_False():
    assert hasAttribute(obj, "name") == False

@pytest.mark.unit
def test_hasAttribute_None():
    assert hasAttribute(None, "name") == False