from flasgger import Schema, fields

class InstancesInput(Schema):
    content = fields.Str()

class ParametersInput(Schema):
    weight = fields.Str(required=True)


# Schema for API
class InferenceParamsSchema(Schema):
    instances = fields.Nested(InstancesInput, many=True, required=True)
    parameters = fields.Nested(ParametersInput)


class PredictionSchema(Schema):
    predictions =  fields.List(fields.Str())

class HealthSchema(Schema):
    status = fields.Str()