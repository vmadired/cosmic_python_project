from typing import List

from allocation.domain.models.batch import Batch
from allocation.domain.models.order import Order
from allocation.exceptions.out_of_stock_ex import OutOfStockEx


def allocate(order: Order, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order))
        batch.allocate(order)
        return batch.reference
    except StopIteration:
        raise OutOfStockEx(order.sku)
