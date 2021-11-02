from typing import List

from allocation.domain.exceptions.out_of_stock_ex import OutOfStockEx
from allocation.domain.model.batch import Batch
from allocation.domain.model.order import Order


def allocate(order: Order, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order))
        batch.allocate(order)
        return batch.reference
    except StopIteration:
        raise OutOfStockEx(order.sku)
