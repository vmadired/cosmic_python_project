from sqlalchemy import Column, Date, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

from allocation.domain.model import batch, order

metadata = MetaData()

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(256)),
    Column("qty", Integer, nullable=False),
    Column("order_id", String(256))
)

batches = Table(
    "batches",
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(256)),
    Column("purchased_qty", Integer, nullable=False),
    Column("eta", Date),
    Column("reference", String(256)),
)

allocations = Table(
    "allocations",
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", String(256)),
    Column("batch_id", String(256))
)


def start_mappers():
    orders_mapper = mapper(order.Order, orders)
    mapper(
        batch.Batch,
        batches,
        properties={
            "_allocations": relationship(
                orders_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
