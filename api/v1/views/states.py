#!/usr/bin/python3
""" View for State objects """

from crypt import methods
from models.base_model import *
from api.v1.views import app_views
from models import storage
from models.state import *
from flask import jsonify, abort, request, make_response


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states():
    """Function that retrieve and save a new State"""
    ls = []
    states = storage.all('State').values()
    if request.method == "GET":
        for state in states:
            ls.append(state.to_dict())
        return jsonify(ls)
    elif request.method == "POST":
        if not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        elif 'name' not in request.json:
            return make_response(jsonify({'error': "Missing name"}), 400)
        else:
            new = State(**request.json)
            new.save()
            return make_response(new.to_dict(), 201)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state(state_id):
    """Function that retrieve, delete and put a State"""
    state = storage.get(State, state_id)
    if state:
        if request.method == "GET":
            return state.to_dict()
        elif request.method == "DELETE":
            storage.delete(state)
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
                        setattr(state, key, value)
                state.updated_at = datetime.utcnow()
                storage.save()
                return make_response(state.to_dict(), 200)
    """If state_id is not linked to a State object"""
    abort(404)
