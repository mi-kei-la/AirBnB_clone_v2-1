#!/usr/bin/python3
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from os import environ, getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Not found"), 404


@app.teardown_appcontext
def teardown_everything(self):
    """Close database."""
    storage.close()

if __name__ == "__main__":
    my_port = getenv('HBNB_API_PORT', 5000)
    my_host = getenv('HBNB_API_HOST', '0.0.0.0')
    app.run(host=my_host, port=my_port, threaded=True)
