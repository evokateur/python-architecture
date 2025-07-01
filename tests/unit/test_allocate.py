from datetime import date, timedelta
from domain.model import allocate, Batch, OrderLine, OutOfStock
import pytest

today = date.today()
tomorrow = today + timedelta(days=1)
later = today + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("batch-001", "SMALL-TABLE", 100, eta=None)
    shipment_batch = Batch("batch-002", "SMALL-TABLE", 100, eta=tomorrow)
    order_line = OrderLine("order-123", "SMALL-TABLE", 10)

    allocate(order_line, [shipment_batch, in_stock_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest_batch = Batch("batch-001", "SMALL-TABLE", 100, eta=today)
    medium_batch = Batch("batch-002", "SMALL-TABLE", 100, eta=tomorrow)
    latest_batch = Batch("batch-003", "SMALL-TABLE", 100, eta=later)

    line = OrderLine("order-123", "SMALL-TABLE", 10)

    allocate(line, [latest_batch, medium_batch, earliest_batch])

    assert earliest_batch.available_quantity == 90
    assert medium_batch.available_quantity == 100
    assert latest_batch.available_quantity == 100


def test_returns_allocated_batch():
    in_stock_batch = Batch("batch-001", "SMALL-TABLE", 100, eta=None)
    shipment_batch = Batch("batch-002", "SMALL-TABLE", 100, eta=tomorrow)
    order_line = OrderLine("order-123", "SMALL-TABLE", 10)

    allocated_batch_ref = allocate(order_line, [shipment_batch, in_stock_batch])

    assert allocated_batch_ref == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch-001", "SMALL-TABLE", 2, eta=today)
    allocate(OrderLine("order-123", "SMALL-TABLE", 2), [batch])

    with pytest.raises(OutOfStock):
        allocate(OrderLine("order-124", "SMALL-TABLE", 2), [batch])
