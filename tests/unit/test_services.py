import pytest
from datetime import date, timedelta

from allocation.service_layer import services
from allocation.service_layer.unit_of_work import AbstractUnitOfWork
from allocation.adapters.repository import AbstractRepository

today = date.today()
tomorrow = today + timedelta(days=1)
later = today + timedelta(days=10)


class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference: str):
        return next(batch for batch in self._batches if batch.reference == reference)

    def list(self):
        return list(self._batches)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_returns_allocation():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "COMPLICATED_LAMP", 100, None, uow)
    result = services.allocate("o1", "COMPLICATED_LAMP", 10, uow)
    assert result == "b1"


def test_error_for_invalid_sku():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "COMPLICATED_LAMP", 100, None, uow)
    with pytest.raises(services.InvalidSku, match="Invalid sku UNREAL_SKU"):
        services.allocate("o1", "UNREAL_SKU", 10, uow)


def test_commits():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "OMINOUS_MIRROR", 100, None, uow)
    services.allocate("o1", "OMINOUS_MIRROR", 10, uow)

    assert uow.committed is True


def test_add_batch():
    uow = FakeUnitOfWork()

    services.add_batch("b1", "ADORABLE-SETTEE", 100, None, uow)
    assert uow.batches.get("b1") is not None
    assert uow.committed is True


def test_deallocate_decrements_available_quantity():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "BLUE-PLINTH", 100, None, uow)

    services.allocate("o1", "BLUE-PLINTH", 10, uow)
    batch = uow.batches.get(reference="b1")
    assert batch.available_quantity == 90

    services.deallocate("o1", "BLUE-PLINTH", 10, uow)
    batch = uow.batches.get(reference="b1")
    assert batch.available_quantity == 100


def test_deallocate_decrements_correct_quantity():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "WHOLE_LOTTA_ROSES", 50, None, uow)
    services.add_batch("b2", "WHOLE_LOTTA_ROSES", 50, None, uow)

    batch_ref = services.allocate("o1", "WHOLE_LOTTA_ROSES", 10, uow)

    batch = uow.batches.get(reference=batch_ref)
    assert batch.available_quantity == 40

    services.deallocate("o1", "WHOLE_LOTTA_ROSES", 10, uow)

    batch = uow.batches.get(reference=batch_ref)
    assert batch.available_quantity == 50


def test_trying_to_deallocate_unallocated_batch():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "PRIVATE_RESERVE", 100, None, uow)

    with pytest.raises(
        services.DeallocationError,
        match="OrderLine not allocated: order_id=o1, sku=PRIVATE_RESERVE",
    ):
        services.deallocate("o1", "PRIVATE_RESERVE", 10, uow)


def test_prefers_warehouse_batches_to_shipments():
    uow = FakeUnitOfWork()
    services.add_batch("batch-001", "SMALL-TABLE", 100, None, uow)
    services.add_batch("batch-002", "SMALL-TABLE", 100, tomorrow, uow)

    services.allocate("order-123", "SMALL-TABLE", 10, uow)

    in_stock_batch = uow.batches.get(reference="batch-001")
    assert in_stock_batch.available_quantity == 90

    shipment_batch = uow.batches.get(reference="batch-002")
    assert shipment_batch.available_quantity == 100
