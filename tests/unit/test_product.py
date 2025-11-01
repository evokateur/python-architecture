from datetime import date, timedelta
from allocation.domain.model import Batch, OrderLine, OutOfStock, Product
import pytest

today = date.today()
tomorrow = today + timedelta(days=1)
later = today + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("batch-001", "SMALL-TABLE", 100, eta=None)
    shipment_batch = Batch("batch-002", "SMALL-TABLE", 100, eta=tomorrow)
    product = Product(sku="SMALL-TABLE", batches=[shipment_batch, in_stock_batch])
    order_line = OrderLine("order-123", "SMALL-TABLE", 10)

    product.allocate(order_line)

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest_batch = Batch("batch-001", "SMALL-TABLE", 100, eta=today)
    medium_batch = Batch("batch-002", "SMALL-TABLE", 100, eta=tomorrow)
    latest_batch = Batch("batch-003", "SMALL-TABLE", 100, eta=later)
    product = Product(sku="SMALL-TABLE", batches=[latest_batch, medium_batch, earliest_batch])
    line = OrderLine("order-123", "SMALL-TABLE", 10)

    product.allocate(line)

    assert earliest_batch.available_quantity == 90
    assert medium_batch.available_quantity == 100
    assert latest_batch.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("batch-001", "SMALL-TABLE", 100, eta=None)
    shipment_batch = Batch("batch-002", "SMALL-TABLE", 100, eta=tomorrow)
    product = Product(sku="SMALL-TABLE", batches=[shipment_batch, in_stock_batch])
    order_line = OrderLine("order-123", "SMALL-TABLE", 10)

    batch_ref = product.allocate(order_line)

    assert batch_ref == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch-001", "SMALL-TABLE", 10, eta=today)
    product = Product(sku="SMALL-TABLE", batches=[batch])

    product.allocate(OrderLine("order-123", "SMALL-TABLE", 10))

    with pytest.raises(OutOfStock, match="SMALL-TABLE"):
        product.allocate(OrderLine("order-124", "SMALL-TABLE", 1))


def test_incremental_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", 100, eta=None)
    product = Product(sku="SMALL-TABLE", batches=[batch])

    product.allocate(OrderLine("order-1", "SMALL-TABLE", 20))
    assert batch.available_quantity == 80

    product.allocate(OrderLine("order-2", "SMALL-TABLE", 30))
    assert batch.available_quantity == 50
