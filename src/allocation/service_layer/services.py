from allocation.domain import model
from allocation.service_layer.unit_of_work import AbstractUnitOfWork


class InvalidSku(Exception):
    pass


class DeallocationError(model.DeallocationError):
    pass


class OutOfStock(model.OutOfStock):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(reference: str, sku: str, quantity: int, eta, uow: AbstractUnitOfWork):
    batch = model.Batch(reference, sku, quantity, eta)
    with uow:
        uow.batches.add(batch)
        uow.commit()


def allocate(order_id, sku, quantity, uow: AbstractUnitOfWork) -> str:
    order_line = model.OrderLine(order_id, sku, quantity)

    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(order_line.sku, batches):
            raise InvalidSku(f"Invalid sku {order_line.sku}")

        try:
            batch_ref = model.allocate(order_line, batches)
        except model.OutOfStock as e:
            raise OutOfStock(str(e))

        uow.commit()

    return batch_ref


def deallocate(order_id, sku, quantity, uow: AbstractUnitOfWork) -> str:
    order_line = model.OrderLine(order_id, sku, quantity)

    with uow:
        batches = uow.batches.list()

        try:
            batch_ref = model.deallocate(order_line, batches)
        except model.DeallocationError as e:
            raise DeallocationError(str(e))

        uow.commit()

    return batch_ref
