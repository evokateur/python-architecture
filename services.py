import model
from model import OrderLine
from repository import AbstractRepository


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def add_batch(reference: str, sku: str, quantity: int, eta, repo: AbstractRepository, session):
    batch = model.Batch(reference, sku, quantity, eta)
    repo.add(batch)
    session.commit()

def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()

    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")

    batch_ref = model.allocate(line, batches)
    session.commit()
    return batch_ref

def deallocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()

    batch_ref = model.deallocate(line, batches)
    session.commit()
    return batch_ref
