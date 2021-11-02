from datetime import date, timedelta

import pytest

from allocation.domain.model.allocation import allocate
from allocation.domain.model.batch import Batch
from allocation.domain.model.order import Order

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def prepare_batch_and_line(sku, qty, line_qty):
    return (
        Batch("batch-001", sku, qty, eta=today),
        Order("order-001", sku, line_qty)
    )


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_order = prepare_batch_and_line("TABLE-LAMP", 10, 5)
    assert large_batch.can_allocate(small_order)


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_order = prepare_batch_and_line("TABLE-LAMP", 5, 10)
    assert small_batch.can_allocate(large_order) is False


def test_can_allocate_if_available_equal_to_required():
    eq_batch, eq_order = prepare_batch_and_line("TABLE-LAMP", 10, 10)
    assert eq_batch.can_allocate(eq_order)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "sku-001", 20, today)
    order_line = Order("batch-001", "sku-002", 4)
    assert batch.can_allocate(order_line) is False


def test_can_only_deallocate_allocated_lines():
    batch, order_line = prepare_batch_and_line("TABLE-LAMP", 10, 2)
    batch.allocate(order_line)
    assert batch.available_qty == 8
    batch.deallocate(order_line)
    assert batch.available_qty == 10


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = Order("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_qty == 90
    assert shipment_batch.available_qty == 100


def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = Order("order1", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.available_qty == 90
    assert medium.available_qty == 100
    assert latest.available_qty == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow)
    line = Order("oref", "HIGHBROW-POSTER", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    b1 = Batch("batch-001", "TABLE-LAMP", 10, eta=today)
    o1 = Order("order-001", "TABLE-LAMP", 100)

    with pytest.raises(Exception, match=o1.sku):
        allocate(o1, [b1])
