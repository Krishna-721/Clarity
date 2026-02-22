from app.extensions import db
from datetime import datetime, timezone


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    transactions = db.relationship("Transaction", backref="category", lazy=True)

    def has_transactions(self):
        return any(not t.is_deleted for t in self.transactions)

    def __repr__(self):
        return f"<Category {self.name}>"