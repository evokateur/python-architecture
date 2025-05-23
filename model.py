from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List


@dataclass()
class OrderLine:
    order_id: str
    sku: str
    quantity: int

    def __hash__(self) -> int:
        return hash((self.order_id, self.sku, self.quantity))


class Batch:
    def __init__(self, reference: str, sku: str, quantity: int, eta: Optional[date]):
        self.reference = reference
        self.sku = sku
        self._purchased_quantity = quantity
        self.eta = eta
        self._allocations = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.quantity

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return NotImplemented
        return self.reference == other.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other: Batch) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


class OutOfStock(Exception):
    pass


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(batch for batch in sorted(batches) if batch.can_allocate(line))
    except StopIteration:
        raise OutOfStock(f"Out of stock for {line}")
    else:
        batch.allocate(line)
        return batch.reference
