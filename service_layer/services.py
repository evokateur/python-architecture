from domain import model
from adapters.repository import AbstractRepository


class InvalidSku(Exception):
    pass


class DeallocationError(model.DeallocationError):
    pass


class OutOfStock(model.OutOfStock):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(
    reference: str, sku: str, quantity: int, eta, repo: AbstractRepository, session
):
    batch = model.Batch(reference, sku, quantity, eta)
    repo.add(batch)
    session.commit()


def allocate(order_id, sku, quantity, repo: AbstractRepository, session) -> str:
    order_line = model.OrderLine(order_id, sku, quantity)

    batches = repo.list()
    if not is_valid_sku(order_line.sku, batches):
        raise InvalidSku(f"Invalid sku {order_line.sku}")

    try:
        batch_ref = model.allocate(order_line, batches)
    except model.OutOfStock as e:
        raise OutOfStock(str(e))

    session.commit()
    return batch_ref


def deallocate(order_id, sku, quantity, repo: AbstractRepository, session) -> str:
    order_line = model.OrderLine(order_id, sku, quantity)

    batches = repo.list()

    try:
        batch_ref = model.deallocate(order_line, batches)
    except model.DeallocationError as e:
        raise DeallocationError(str(e))

    session.commit()
    return batch_ref
