#!/usr/bin/python3
""" View for State objects """

from crypt import methods
from models.base_model import *
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import *
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_state(state_id):
    """Function that retrieve and save a new City object"""
    state = storage.get(State, state_id)
    cities = storage.all('City').values()
    cities_list = []
    if state:
        for city in cities:
            if city.state_id == state_id:
                cities_list.append(city.to_dict())
        if request.method == "GET":
            return jsonify(cities_list)
        elif request.method == "POST":
            if not request.json:
                return make_response(jsonify(
                                     {'error': "Not a JSON"}), 400)
            elif 'name' not in request.json:
                return make_response(jsonify(
                                     {'error': "Missing name"}), 400)
            else:
                r_json = request.json
                r_json['state_id'] = state_id
                new = City(**r_json)
                new.save()
                return make_response(new.to_dict(), 201)
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def city(city_id):
    """Function that retrieve, delete and put a City"""
    city = storage.get(City, city_id)
    if city:
        if request.method == "GET":
            return city.to_dict()
        elif request.method == "DELETE":
            storage.delete(city)
            storage.save()
            return {}
        elif request.method == "PUT":
            if not request.json:
                return make_response(jsonify({'error': "Not a JSON"}), 400)
            else:
                r_json = request.json
                for key, value in r_json.items():
                    if key != 'id' and key != 'state_id' and\
                       key != 'created_at' and key != "updated_at":
                        setattr(city, key, value)
                city.updated_at = datetime.utcnow()
                storage.save()
                return make_response(city.to_dict(), 200)
    abort(404)
