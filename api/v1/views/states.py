#!/usr/bin/python3
""" This module handles all views of State objects.
"""
from models import storage
from flask import Flask, jsonify, request
from api.v1.views import app_views
from models.base_model import BaseModel
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def ret_all_states():
    """Retrieve a list of all state object dictionaries"""
    all_states = []
    for obj in storage.all(State).values():
        all_states.append(obj.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def ret_state(state_id):
    """Retrieve a specific state dictionary.
    Raise 404 error if state_id is not linked to a State object.
    """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a specific state dictionary.
    Raise 404 error if state_id is not linked to a State object,
    otherwise return an empty dictionary with status code 200.
    """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """Create a new State object and add to storage.
    Raise error 400 if request body is not JSON format,
    or if no name is given. Return the new State with
    status code 201.
    """
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    elif user_input.get('name') is None:
        abort(400, {'message': 'Missing name'})
    else:
        obj = State(**user_input)
        storage.new(obj)
        storage.save()
        state_obj = obj.to_dict()
        return jsonify(state_obj), 201
    abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a State object. Raise 404 error if state_id
    is not linked to a state object, 400 if the request body
    is not valid JSON data. Return State dictionary with
    status code 200 otherwise.
    """
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    obj = storage.get(State, state_id)
    for k, v in user_input.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
