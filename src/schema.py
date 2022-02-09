from flasgger import Schema, fields

# Optional marshmallow support
class HealthSchema(Schema):
    status = fields.Str()