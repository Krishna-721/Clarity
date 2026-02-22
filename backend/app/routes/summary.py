from flask import Blueprint, jsonify
from app.extensions import db
from app.models.transaction import Transaction
from app.models.category import Category
from sqlalchemy import func

summary_bp = Blueprint("summary", __name__)


@summary_bp.route("/", methods=["GET"])
def get_summary():
    results = (
        db.session.query(
            Category.id,
            Category.name,
            func.sum(Transaction.amount).label("total"),
            func.count(Transaction.id).label("count")
        )
        .join(Transaction, Transaction.category_id == Category.id)
        .filter(Transaction.is_deleted == False)
        .filter(Category.is_deleted == False)
        .group_by(Category.id, Category.name)
        .all()
    )

    breakdown = [
        {
            "category_id": r.id,
            "category_name": r.name,
            "total_spent": round(r.total, 2),
            "transaction_count": r.count
        }
        for r in results
    ]

    overall_total = sum(r["total_spent"] for r in breakdown)

    return jsonify({
        "overall_total": round(overall_total, 2),
        "breakdown": breakdown
    }), 200