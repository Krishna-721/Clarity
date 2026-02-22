from marshmallow import Schema, fields, validate, validates, ValidationError


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(load_default=None, validate=validate.Length(max=255))
    created_at = fields.DateTime(dump_only=True)
    is_deleted = fields.Bool(dump_only=True)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Name cannot be blank or whitespace.")