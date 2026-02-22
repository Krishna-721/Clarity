from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models.category import Category
from app.schemas.category_schema import CategorySchema

categories_bp = Blueprint("categories", __name__)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@categories_bp.route("/", methods=["GET"])
def get_categories():
    categories = Category.query.filter_by(is_deleted=False).all()
    return jsonify(categories_schema.dump(categories)), 200


@categories_bp.route("/", methods=["POST"])
def create_category():
    try:
        data = category_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

    existing = Category.query.filter_by(name=data["name"], is_deleted=False).first()
    if existing:
        return jsonify({"errors": {"name": ["Category with this name already exists."]}}), 409

    category = Category(**data)
    db.session.add(category)
    db.session.commit()
    return jsonify(category_schema.dump(category)), 201


@categories_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id, is_deleted=False).first()
    if not category:
        return jsonify({"error": "Category not found."}), 404

    if category.has_transactions():
        return jsonify({
            "error": "Cannot delete a category that has transactions. Reassign or delete transactions first."
        }), 409

    category.is_deleted = True
    db.session.commit()
    return jsonify({"message": "Category deleted."}), 200