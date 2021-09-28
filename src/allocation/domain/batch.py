from dataclasses import dataclass
from datetime import date
from typing import Optional

from allocation.domain.order_line import OrderLine


@dataclass()
class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.purchased_qty = qty
        self.eta = eta
        self._allocations = set()  # store in set until db integration

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    @property
    def available_qty(self) -> int:
        return self.purchased_qty - self.allocated_qty

    @property
    def allocated_qty(self) -> int:
        return sum(line.qty for line in self._allocations)

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if (line in self._allocations):
            self._allocations.remove(line)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.available_qty >= line.qty and self.sku == line.sku and not self._has_allocation(line)

    def _has_allocation(self, line: OrderLine) -> bool:
        for allocation in self._allocations:
            if line.orderid == allocation.orderid:
                return True
        return False
