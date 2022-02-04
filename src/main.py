from flask import Flask
from . import config

app = Flask(__name__)

@app.route("/", methods=['GET'])
def health():
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(config.APP_PORT))