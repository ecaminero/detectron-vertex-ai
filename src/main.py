from urllib import request
from . import config, inference
from .inference import prediction
from flask import Flask, jsonify
from apispec import APISpec
from flasgger import Swagger, apispec_to_template, validate
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from .schema import HealthSchema, InferenceParamsSchema, PredictionSchema

app = Flask(__name__)

# Create an API Specification
spec = APISpec(
    title='Image Detectron Vertex-AI',
    version='1.0.10',
    openapi_version='2.0.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)


@app.route("/health", methods=["GET"])
def health():
    """
    HealthCheck.
    ---
    description: HealthCheck App endpoint
    responses:
        200:
            description: Status check
            schema:
                $ref: '#/definitions/Health'
    """    
    check = dict(status = "OK")
    return HealthSchema().dump(check)


@app.route("/inference", methods=["POST"])
def inference():
    """
    Inference endpoint.
    ---
    post:
        description: HealthCheck App endpoint
        parameters:
          - name: prediction
            in: body
            required: True
            schema:
                $ref: '#/definitions/InferenceParams'
    responses:
        201:
            description: A pet to be returned
            schema:
                $ref: '#/definitions/Prediction'
    """
    print(request) 
    result = prediction()
    return jsonify(result)


template = apispec_to_template(
    app=app,
    spec=spec,
    definitions=[
        HealthSchema, 
        InferenceParamsSchema,
        PredictionSchema
    ],
    paths=[health, inference]

)

swag = Swagger(app, template=template)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(config.APP_PORT))