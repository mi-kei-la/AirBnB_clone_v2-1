#!/usr/bin/python3
""" This module handles all views of Amenity objects.
"""
from models import storage
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models.base_model import BaseModel
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def ret_all_users():
    """Retrieve a list of all User object dictionaries"""
    all_users = []
    for obj in storage.all(User).values():
        all_users.append(obj.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def ret_amenity(user_id):
    """Retrieve a specific user dictionary.
    Raise 404 error if user_id is not linked to a User object.
    """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a specific user from storage.
    Raise 404 error if user_id is not linked to an User object,
    otherwise return an empty dictionary with status code 200.
    """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """Create a new User object and add to storage.
    Raise error 400 if request body is not JSON format,
    or if no email or password are given. Return the new
    User with status code 201.
    """
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    elif user_input.get('email') is None:
        abort(400, {'message': 'Missing email'})
    elif user_input.get('password') is None:
        abort(400, {'message': 'Missing password'})
    else:
        obj = User(**user_input)
        storage.new(obj)
        storage.save()
        user_obj = obj.to_dict()
        return jsonify(user_obj), 201
    abort(404)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a User object. Raise 404 error if user_id
    is not linked to a user object, 400 if the request body
    is not valid JSON data. Return User dictionary with
    status code 200 otherwise.
    """
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    obj = storage.get(User, user_id)
    for k, v in user_input.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
