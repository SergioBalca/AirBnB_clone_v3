#!/usr/bin/python3
""" View for State objects """

from crypt import methods
from models.base_model import *
from api.v1.views import app_views
from models import storage
from models.state import *
from flask import jsonify, abort, request, make_response


@app_views.route('/states', strict_slashes=False)
def get_states():
    """Retrives all State objects"""
    state_list = []
    states = storage.all('State').values()
    for state in states:
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<int: state_id>', strict_slashes=False)
def get_state_by_id(state_id):
    """Retrives a State object"""
    state = storage.get(State, state_id)
    if state:
        return state.to_dict()
    """Raises an error 404 if id is not linked to an State"""
    abort(404)


@app_views.route('/states/<int: state_id>', strict_slashes=False,
                 methods='DELETE')
def delete_state(state_id):
    """Adds a new State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return {}
    """Raises an error 404 if id is not linked to an State"""
    abort(404)


@app_views.route('/states', strict_slashes=False, methods='POST')
def post_state():
    """Adds new State object"""
    if not request.json:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    elif 'name' not in request.json:
        return make_response(jsonify({'error': "Missing name"}), 400)
    else:
        new = State(**request.json)
        new.save()
        return make_response(new.to_dict(), 201)


@app_views.route('/states/<int: state_id>', strict_slashes=False,
                 methods='PUT')
def update_state(state_id):
    """Updates an State object"""
    state = storage.get(State, state_id)
    if state:
        if not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        else:
            r_json = request.json
            for key, value in r_json.items():
                if key != 'id' and key != 'created_at' and\
                   key != "updated_at":
                    setattr(state, key, value)
            state.updated_at = datetime.utcnow()
            storage.save()
            return make_response(state.to_dict(), 200)
    abort(404)
