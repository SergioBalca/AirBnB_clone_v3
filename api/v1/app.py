#!/usr/bin/python3
"""Flask app"""

from os import getenv
from threading import Thread
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """ method to handle teardown_appcontext
        that calls storage.close()
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """handler for 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":

    hbnb_api_host = getenv("HBNB_API_HOST")
    hbnb_api_port = getenv("HBNB_API_PORT")

    app.run(host=hbnb_api_host, port=hbnb_api_port, threaded=True)
