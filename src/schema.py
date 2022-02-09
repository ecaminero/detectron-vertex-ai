from flasgger import Schema, fields

class InstancesInput(Schema):
    content = fields.Str()

class ParametersInput(Schema):
    weight = fields.Str(required=True)

class PredictionsResponseSchema(Schema):
    weight = fields.Str()


# Schema for API
class InferenceParamsSchema(Schema):
    instances = fields.Nested(InstancesInput, many=True, required=True)
    parameters = fields.Nested(ParametersInput)


class PredictionSchema(Schema):
    predictions =  fields.List(fields.Str())
    deployedModelId = fields.Str()
    model = fields.Str()
    modelDisplayName = fields.Str()

class HealthSchema(Schema):
    status = fields.Str()