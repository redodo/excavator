import pytest

from dirtcastle.annotators import registry


@pytest.fixture(autouse=True)
def clear_annotator_registry():
    """Removes annotators that have been defined inside tests"""
    snapshot = registry.copy()
    yield
    for diff in registry ^ snapshot:
        registry.remove(diff)
