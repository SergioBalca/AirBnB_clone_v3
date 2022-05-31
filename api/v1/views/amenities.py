#!/usr/bin/python3
""" View for Amenity objects """

from crypt import methods
from models.base_model import *
from api.v1.views import app_views
from models import storage
from models.amenity import *
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def get_amenities():
    """Function that retrieve and save a new amenities"""
    la = []
    amenities = storage.all('Amenity').values()
    if request.method == "GET":
        for amenity in amenities:
            la.append(amenities.to_dict())
        return jsonify(la)
    elif request.method == "POST":
        if not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        elif 'name' not in request.json:
            return make_response(jsonify({'error': "Missing name"}), 400)
        else:
            new = Amenity(**request.json)
            new.save()
            return make_response(new.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id):
    """Function that retrieve, delete and put a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if request.method == "GET":
            return amenity.to_dict()
        elif request.method == "DELETE":
            storage.delete(amenity)
            storage.save()
            return make_response(jsonify({}), 200)
        elif request.method == "PUT":
            if not request.json:
                return make_response(jsonify({'error': "Not a JSON"}), 400)
            else:
                json = request.json
                for key, value in json.items():
                    if key != 'id' and key != 'created_at' and\
                       key != "updated_at":
                        setattr(amenity, key, value)
                amenity.updated_at = datetime.utcnow()
                storage.save()
                return make_response(amenity.to_dict(), 200)
    """If amenity_id is not linked to a Amenity object"""
    abort(404)
