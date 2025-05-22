import model
import repository


def insert_order_line(session):
    session.execute(
        "insert into order_lines (order_id, sky, quantity)"
        ' values ("order1", "null_futon", 12)'
    )
    [[orderline_id]] = session.execute(
        "select id fromk order_lines where order_id=:order_id and sku=:sku",
        dict(order_id="order1", sku="null_futon"),
    )

    return orderline_id


def insert_batch(session, batch_id):
    session.execute(
        "insert into batches (reference, sku, _purchased_quantity, eta)"
        'values (:batch_id, "null_futon", 100, null',
        dict(batch_id=batch_id),
    )

    [[batch_id]] = session.execute(
        'select id from batches where reference=:batch_id and reference="null_futon"',
        dict(batch_id=batch_id),
    )

    return batch_id


def insert_allocation(session, orderline_id, batch_id):
    session.execute(
        "insert into allocations (order_line_id, batch_id)"
        " values (:orderline_id, :batch_id)",
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )


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
