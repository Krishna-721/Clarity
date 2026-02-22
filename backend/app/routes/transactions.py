from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.transaction_schema import TransactionSchema

transactions_bp = Blueprint("transactions", __name__)
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)


@transactions_bp.route("/", methods=["GET"])
def get_transactions():
    query = Transaction.query.filter_by(is_deleted=False)

    category_id = request.args.get("category_id", type=int)
    if category_id:
        query = query.filter_by(category_id=category_id)

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    transactions = query.order_by(Transaction.date.desc()).all()
    return jsonify(transactions_schema.dump(transactions)), 200


@transactions_bp.route("/", methods=["POST"])
def create_transaction():
    try:
        data = transaction_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

    category = Category.query.filter_by(id=data["category_id"], is_deleted=False).first()
    if not category:
        return jsonify({"errors": {"category_id": ["Category not found or has been deleted."]}}), 404

    transaction = Transaction(**data)
    db.session.add(transaction)
    db.session.commit()
    return jsonify(transaction_schema.dump(transaction)), 201


@transactions_bp.route("/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    transaction = Transaction.query.filter_by(id=transaction_id, is_deleted=False).first()
    if not transaction:
        return jsonify({"error": "Transaction not found."}), 404

    transaction.is_deleted = True
    db.session.commit()
    return jsonify({"message": "Transaction deleted."}), 200