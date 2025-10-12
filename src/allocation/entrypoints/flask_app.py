from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from allocation import config
from allocation.adapters import orm
from allocation.adapters import repository
from allocation.service_layer import services

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


@app.route("/batches", methods=["POST"])
def post_batch_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    reference = request.json["reference"]
    sku = request.json["sku"]
    quantity = int(request.json["quantity"])
    eta = request.json.get("eta") or None

    services.add_batch(reference, sku, quantity, eta, repo, session)

    return "OK", 201


@app.route("/allocations", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    order_id, sku, quantity = (
        request.json["order_id"],
        request.json["sku"],
        request.json["quantity"],
    )

    try:
        batch_ref = services.allocate(order_id, sku, quantity, repo, session)
    except (services.OutOfStock, services.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batch_ref": batch_ref}), 201


@app.route("/allocations", methods=["DELETE"])
def deallocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    order_id, sku, quantity = (
        request.json["order_id"],
        request.json["sku"],
        request.json["quantity"],
    )

    try:
        batch_ref = services.deallocate(order_id, sku, quantity, repo, session)
    except services.DeallocationError as e:
        return jsonify({"message": str(e)}), 400

    return "OK", 200
