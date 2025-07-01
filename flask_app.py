from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import model
import orm
import repository
import services

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

@app.route("/batch", methods=["POST"])
def post_batch_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    reference = request.json["reference"]
    sku = request.json["sku"]
    quantity = int(request.json["quantity"])
    eta = request.json.get("eta") or None

    services.add_batch(reference, sku, quantity, eta, repo, session)

    return jsonify({"message": "Batch created successfully"}), 201

@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json["order_id"],
        request.json["sku"],
        request.json["quantity"],
    )

    try:
        batch_ref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batch_ref": batch_ref}), 201

@app.route("/deallocate", methods=["POST"])
def deallocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    line = model.OrderLine(
        request.json["order_id"],
        request.json["sku"],
        request.json["quantity"],
    )

    try:
        batch_ref = services.deallocate(line, repo, session)
    except (model.DeallocationError) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batch_ref": batch_ref}), 201
