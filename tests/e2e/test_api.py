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


def post_to_add_batch(reference, sku, quantity, eta=None):
    url = config.get_api_url() + "/batches"
    data = {
        "reference": reference,
        "sku": sku,
        "quantity": quantity,
    }
    if eta:
        data["eta"] = eta
    r = requests.post(url, json=data)
    assert r.status_code == 201, f"Failed to add batch: {r.text}"


@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_201_and_allocated_batch():
    sku, other_sku = random_sku(), random_sku("other")
    early_batch = random_batch_ref("1")
    later_batch = random_batch_ref("2")
    other_batch = random_batch_ref("3")

    post_to_add_batch(later_batch, sku, 100, "2025-01-02")
    post_to_add_batch(early_batch, sku, 100, "2025-01-01")
    post_to_add_batch(other_batch, other_sku, 100, None)

    data = {"order_id": random_order_id(), "sku": sku, "quantity": 3}

    url = config.get_api_url()
    r = requests.post(f"{url}/allocations", json=data)

    assert r.status_code == 201
    assert r.json()["batch_ref"] == early_batch


@pytest.mark.usefixtures("restart_api")
def test_unhappy_path_returns_400_and_error_message():
    unknown_sku, order_id = random_sku(), random_order_id()
    data = {"order_id": order_id, "sku": unknown_sku, "quantity": 20}

    url = config.get_api_url()
    r = requests.post(f"{url}/allocations", json=data)

    assert r.status_code == 400
    assert r.json()["message"] == f"Invalid sku {unknown_sku}"
