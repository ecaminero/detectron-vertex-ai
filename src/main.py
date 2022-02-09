from . import config
from flask import Flask
from flasgger import Swagger
from apispec import APISpec
from flasgger.utils import apispec_to_template
from .schema import HealthSchema
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

app = Flask(__name__)
# Create an APISpec
spec = APISpec(
    title='Flasger Petstore',
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
    A cute furry animal endpoint.
    Get a random pet
    ---
    description: Get a random pet
    responses:
        200:
            description: A pet to be returned
            schema:
                $ref: '#/definitions/Health'
    """    
    check = dict(status = "OK")
    return HealthSchema().dump(check)



template = apispec_to_template(
    app=app,
    spec=spec,
    definitions=[HealthSchema],
    paths=[health]
)

swag = Swagger(app, template=template)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(config.APP_PORT))