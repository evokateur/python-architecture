from datetime import date
from model import Batch, OrderLine


def make_batch_and_line(sku: str, batch_qty: int, line_qty: int):
    return Batch("batch-001", sku, batch_qty, None), OrderLine(
        "order-123", sku, line_qty
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", quantity=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("SMALL-TABLE", 20, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_less_than_required():
    small_batch, large_line = make_batch_and_line("SMALL-TABLE", 2, 20)
    assert not small_batch.can_allocate(large_line)


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 20)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_dont_match():
    batch = Batch("batch-001", "SMALL-TABLE", 20, None)
    line = OrderLine("order-123", "LARGE-TABLE", 2)
    assert not batch.can_allocate(line)


def test_can_only_deallocate_allocated_lines():
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 2)
    batch.deallocate(line)
    assert batch.available_quantity == 20


def test_allocation_is_idempotent():
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_deallocate():
    batch, line = make_batch_and_line("EXPENSIVE-FOOTSTOOL", 20, 2)
    batch.allocate(line)
    batch.deallocate(line)
    assert batch.available_quantity == 20
