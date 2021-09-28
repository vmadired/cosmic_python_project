from datetime import date, timedelta

from allocation.domain.batch import Batch
from allocation.domain.model import allocate
from allocation.domain.order_line import OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def prepare_batch_and_line(sku, qty, line_qty):
    return (
        Batch("batch-001", sku, qty, eta=today),
        OrderLine("order-001", sku, line_qty)
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, order_line = prepare_batch_and_line("TABLE-LAMP", 20, 2)
    batch_1, order_line_1 = prepare_batch_and_line("TABLE-LAMP", 20, 12)
    batch.allocate(order_line)
    batch.allocate(order_line_1)
    assert batch.available_qty == 18




# def test_prefers_warehouse_batches_to_shipments():
#     pytest.fail("todo")
#
#
# def test_prefers_earlier_batches():
#     pytest.fail("todo")
