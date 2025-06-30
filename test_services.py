import model
import pytest
import services
from repository import FakeRepository


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_returns_allocation():
    line = model.OrderLine("o1", "COMPLICATED_LAMP", 10)
    batch = model.Batch("b1", "COMPLICATED_LAMP", 100, None)
    repo = FakeRepository([batch])
    result = services.allocate(line, repo, FakeSession())
    assert result == "b1"


def test_error_for_invalid_sku():
    line = model.OrderLine("o1", "UNREAL_SKU", 10)
    batch = model.Batch("b1", "REAL_SKU", 100, None)
    repo = FakeRepository([batch])
    with pytest.raises(services.InvalidSku, match="Invalid sku UNREAL_SKU"):
        services.allocate(line, repo, FakeSession())


def test_commits():
    line = model.OrderLine("o1", "OMINOUS_MIRROR", 10)
    batch = model.Batch("b1", "OMINOUS_MIRROR", 100, None)
    repo = FakeRepository([batch])
    session = FakeSession()

    services.allocate(line, repo, session)

    assert session.committed is True
