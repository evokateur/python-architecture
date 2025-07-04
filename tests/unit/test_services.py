from domain import model
import pytest
from service_layer import services
from adapters.repository import FakeRepository


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

def test_deallocate_decrements_available_quantity():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("b1", "BLUE-PLINTH", 100, None, repo, session)
    line = model.OrderLine("o1", "BLUE-PLINTH", 10)

    services.allocate(line, repo, session)
    batch = repo.get(reference="b1")
    assert batch.available_quantity == 90

    services.deallocate(line, repo, session)
    batch = repo.get(reference="b1")
    assert batch.available_quantity == 100


def test_deallocate_decrements_correct_quantity():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("b1", "WHOLE_LOTTA_ROSES", 50, None, repo, session)
    services.add_batch("b2", "WHOLE_LOTTA_ROSES", 50, None, repo, session)

    line = model.OrderLine("o1", "WHOLE_LOTTA_ROSES", 10)
    services.allocate(line, repo, session)
    assert model.sku_available_quantity("WHOLE_LOTTA_ROSES", repo.list()) == 90

    services.deallocate(line, repo, session)
    assert model.sku_available_quantity("WHOLE_LOTTA_ROSES", repo.list()) == 100


def test_trying_to_deallocate_unallocated_batch():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("b1", "PRIVATE_RESERVE", 100, None, repo, session)

    line = model.OrderLine("o1", "PRIVATE_RESERVE", 10)
    with pytest.raises(model.DeallocationError, match="OrderLine not allocated: order_id=o1, sku=PRIVATE_RESERVE"):
        services.deallocate(line, repo, session)
