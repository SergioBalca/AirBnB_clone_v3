#!/usr/bin/python3
"""View for User objects"""

from models.base_model import *
from api.v1.views import app_views
from models import storage
from models.user import *
from flask import jsonify, abort, request, make_response


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users():
    """Function that retrieve and save a new User"""
    lu = []
    users = storage.all('User').values()
    if request.method == "GET":
        for user in users:
            lu.append(user.to_dict())
        return jsonify(lu)
    elif request.method == "POST":
        if not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        elif 'email' not in request.json:
            return make_response(jsonify({'error': "Missing email"}), 400)
        elif 'password' not in request.json:
            return make_response(jsonify({'error': "Missing password"}), 400)
        else:
            new = User(**request.json)
            new.save()
            return make_response(new.to_dict(), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user(user_id):
    """Function that retrieve, delete and put an User"""
    user = storage.get(User, user_id)
    if user:
        if request.method == "GET":
            return user.to_dict()
        elif request.method == "DELETE":
            storage.delete(user)
            storage.save()
            return make_response(jsonify({}), 200)
        elif request.method == "PUT":
            if not request.json:
                return make_response(jsonify({'error': "Not a JSON"}), 400)
            else:
                json = request.json
                for key, value in json.items():
                    if key != 'id' and key != 'email' and\
                       key != 'created_at' and key != "updated_at":
                        setattr(user, key, value)
                user.updated_at = datetime.utcnow()
                storage.save()
                return make_response(user.to_dict(), 200)
    abort(404)
