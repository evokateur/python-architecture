from domain import model
from service_layer import unit_of_work
from sqlalchemy import text


def insert_batch(session, ref, sku, qty, eta):
    session.execute(
        text(
            "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
            " VALUES (:ref, :sku, :qty, :eta)"
        ),
        dict(ref=ref, sku=sku, qty=qty, eta=eta),
    )


def get_allocated_batch_ref(session, order_id, sku):
    [[order_line_id]] = session.execute(
        text("SELECT id FROM order_lines where order_id=:order_id AND sku=:sku"),
        dict(order_id=order_id, sku=sku),
    )
    [[batch_ref]] = session.execute(
        text(
            "SELECT b.reference FROM allocations JOIN batches b ON batch_id = b.id"
            " WHERE order_line_id=:order_line_id"
        ),
        dict(order_line_id=order_line_id),
    )
    return batch_ref


def test_uow_can_retrieve_a_batch_and_allocate_to_it(session_factory):
    session = session_factory()
    insert_batch(session, "batch1", "HIPSTER-WORKBENCH", 100, None)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        batch = uow.batches.get(reference="batch1")
        line = model.OrderLine("order1", "HIPSTER-WORKBENCH", 10)
        batch.allocate(line)
        uow.commit()

    batch_ref = get_allocated_batch_ref(session, "order1", "HIPSTER-WORKBENCH")
    assert batch_ref == "batch1"
