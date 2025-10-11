from allocation.domain import model
from allocation.adapters import repository
from sqlalchemy import text


def insert_order_line(session):
    session.execute(
        text(
            "INSERT INTO order_lines (order_id, sku, quantity) VALUES (:order_id, :sku, :quantity)"
        ),
        {"order_id": "order1", "sku": "null_futon", "quantity": 12},
    )
    session.commit()

    result = session.execute(
        text("SELECT id FROM order_lines WHERE order_id = :order_id AND sku = :sku"),
        {"order_id": "order1", "sku": "null_futon"},
    )

    return result.scalar_one()


def insert_batch(session, batch_id):
    session.execute(
        text(
            "INSERT INTO batches (reference, sku, _purchased_quantity, eta) "
            "VALUES (:batch_id, :sku, :quantity, :eta)"
        ),
        {"batch_id": batch_id, "sku": "null_futon", "quantity": 100, "eta": None},
    )
    session.commit()

    result = session.execute(
        text("SELECT id FROM batches WHERE reference = :batch_id AND sku = :sku"),
        {"batch_id": batch_id, "sku": "null_futon"},
    )

    return result.scalar_one()


def insert_allocation(session, order_line_id, batch_id):
    session.execute(
        text(
            "INSERT INTO allocations (order_line_id, batch_id) "
            "VALUES (:orderline_id, :batch_id)"
        ),
        {"orderline_id": order_line_id, "batch_id": batch_id},
    )
    session.commit()


def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch-001", "sku-001", 100, None)
    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    saved_batch = session.query(model.Batch).filter_by(reference="batch-001").one()
    assert saved_batch == batch
    assert saved_batch.sku == "sku-001"
    assert saved_batch._purchased_quantity == 100
    assert saved_batch.eta is None


def test_repository_can_retrieve_a_batch_with_allocations(session):
    order_line_id = insert_order_line(session)
    batch_id = insert_batch(session, "batch-001")
    insert_batch(session, "batch-002")
    insert_allocation(session, order_line_id, batch_id)

    repo = repository.SqlAlchemyRepository(session)
    retrieved_batch = repo.get("batch-001")
    expected_batch = model.Batch("batch-001", "null_futon", 100, None)

    assert retrieved_batch.sku == expected_batch.sku
    assert retrieved_batch._allocations == {model.OrderLine("order1", "null_futon", 12)}
