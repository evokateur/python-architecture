from datetime import date, timedelta
from model import allocate, Batch, OrderLine, OutOfStock
import pytest

today = date.today()
tomorrow = today + timedelta(days=1)
later = today + timedelta(days=10)


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch-001", "SMALL-TABLE", 2, eta=today)
    allocate(OrderLine("order-123", "SMALL-TABLE", 2), [batch])

    with pytest.raises(OutOfStock):
        allocate(OrderLine("order-124", "SMALL-TABLE", 2), [batch])
