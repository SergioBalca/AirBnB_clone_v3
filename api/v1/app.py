#!/usr/bin/python3
"""Flask app"""

from os import getenv
from threading import Thread
from models import storage
from api.v1.views import app_views
from flask import Flask

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """ method to handle teardown_appcontext
        that calls storage.close()
    """
    storage.close()


if __name__ == "__main__":

    hbnb_api_host = getenv("HBNB_API_HOST")
    hbnb_api_port = getenv("HBNB_API_PORT")

    app.run(host=hbnb_api_host, port=hbnb_api_port, threaded=True)
