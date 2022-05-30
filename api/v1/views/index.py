#!/usr/bin/python3
""" Index view module """
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns status of API"""
    return jsonify({"status": "OK"})
