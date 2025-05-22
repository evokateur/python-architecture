from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import properties, registry, relationship
import model

metadata = MetaData()
mappery = registry()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("quantity", Integer, nullable=False),
    Column("order_id", String(255)),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255), nullable=False),
    Column("order_id", String(255), ForeignKey("order_lines.order_id")),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_line_id", ForeignKey("order_lines.id"), nullable=False),
    Column("batch_id", ForeignKey("batches.id"), nullable=False),
)


def start_mappers():
    mappery.map_imperatively(model.OrderLine, order_lines)
    mappery.map_imperatively(
        model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                model.OrderLine,
                secondary=allocations,
                collection_class=set,
            ),
        },
    )
