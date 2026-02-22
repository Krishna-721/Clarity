from marshmallow import Schema, fields, validate, validates, ValidationError


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    amount = fields.Float(required=True)
    date = fields.Date(required=True)
    category_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    is_deleted = fields.Bool(dump_only=True)

    category = fields.Nested(lambda: CategoryNestedSchema(), dump_only=True)

    @validates("amount")
    def validate_amount(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("Amount must be greater than zero.")


class CategoryNestedSchema(Schema):
    id = fields.Int()
    name = fields.Str()