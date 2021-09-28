from typing import List

from allocation.domain.batch import Batch
from allocation.domain.order_line import OrderLine
from allocation.exceptions.out_of_stock_ex import OutOfStockEx


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStockEx(line.sku)
