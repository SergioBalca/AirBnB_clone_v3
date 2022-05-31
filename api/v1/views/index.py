#!/usr/bin/python3
""" Index view module """
from itertools import count
from models import storage
import json
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns status of API"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns the number of each object by type"""
    classes = {"users": "User", "states": "State", "amenities": "Amenity",
               "cities": "City", "places": "Place", "reviews": "Review"}
    obj_dict = {}
    for key, value in classes.items():
        obj_dict[key] = storage.count(value)
    return obj_dict
