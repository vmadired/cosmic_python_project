from dataclasses import dataclass
from datetime import date
from typing import Optional

from allocation.domain.model.order import Order


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
        return sum(order.qty for order in self._allocations)

    def allocate(self, order: Order):
        if self.can_allocate(order):
            self._allocations.add(order)

    def deallocate(self, order: Order):
        if (order in self._allocations):
            self._allocations.remove(order)

    def can_allocate(self, order: Order) -> bool:
        return self.available_qty >= order.qty and self.sku == order.sku and not self._has_allocation(order)

    def _has_allocation(self, order: Order) -> bool:
        for allocation in self._allocations:
            if order.order_id == allocation.order_id:
                return True
        return False
