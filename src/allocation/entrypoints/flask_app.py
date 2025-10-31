from flask import Flask, request, jsonify

from allocation.adapters import orm
from allocation.service_layer import services
from allocation.service_layer.unit_of_work import SqlAlchemyUnitOfWork

orm.start_mappers()
app = Flask(__name__)


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


@app.route("/batches", methods=["POST"])
def post_batch_endpoint():
    uow = SqlAlchemyUnitOfWork()

    reference = request.json["reference"]
    sku = request.json["sku"]
    quantity = int(request.json["quantity"])
    eta = request.json.get("eta") or None

    services.add_batch(reference, sku, quantity, eta, uow)

    return "OK", 201


@app.route("/allocations", methods=["POST"])
def allocate_endpoint():
    uow = SqlAlchemyUnitOfWork()

    order_id, sku, quantity = (
        request.json["order_id"],
        request.json["sku"],
        request.json["quantity"],
    )

    try:
        batch_ref = services.allocate(order_id, sku, quantity, uow)
    except (services.OutOfStock, services.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batch_ref": batch_ref}), 201


@app.route("/allocations", methods=["DELETE"])
def deallocate_endpoint():
    uow = SqlAlchemyUnitOfWork()

    order_id, sku, quantity = (
        request.json["order_id"],
        request.json["sku"],
        request.json["quantity"],
    )

    try:
        services.deallocate(order_id, sku, quantity, uow)
    except services.DeallocationError as e:
        return jsonify({"message": str(e)}), 400

    return "OK", 200
