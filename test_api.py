import uuid
import pytest
import requests

import config


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{'-' + name if name else ''}{random_suffix()}"


def random_batch_ref(name=""):
    return f"batch-{'-' + name if name else ''}{random_suffix()}"


def random_order_id(name=""):
    return f"order-{'-' + name if name else ''}{random_suffix()}"


@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocation(add_stock):
    sku, other_sku = random_sku(), random_sku("other")
    early_batch = random_batch_ref("1")
    later_batch = random_batch_ref("2")
    other_batch = random_batch_ref("3")
    add_stock(
        [
            (later_batch, sku, 100, "2025-01-02"),
            (early_batch, sku, 100, "2025-01-01"),
            (other_batch, other_sku, 100, None),
        ]
    )
    data = {"order_id": random_order_id(), "sku": sku, "quantlty": 3}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)
    assert r.status_code == 201
    assert r.json()["batch_ref"] == early_batch
