#!/usr/bin/python3
""" This module handles all views of City objects.
"""
from models import storage
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models.base_model import BaseModel
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """Retrieve all cities of the state linked to a given state id.
    Raise 404 error otherwise"""
    if storage.get(State, state_id) is None:
        abort(404)
    city_dict = storage.all(City)
    city_list = []
    for city in city_dict.values():
        if city.state_id == state_id:
            city = city.to_dict()
            city_list.append(city)
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieve City object linked to a given id. Raise 404 otherwise."""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete City from storage. If successful, return empty
    dictionary with status code 200, otherwise raise 404 error.
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_city(state_id):
    """Create a new City object related to the given state,
    and add to storage. Raise error 400 if request body is
    not JSON format, or if no name is given.
    Return the new State with status code 201.
    """
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    elif user_input.get('name') is None:
        abort(400, {'message': 'Missing name'})
    else:
        if storage.get(State, state_id) is None:
            abort(404)
        obj = City(**user_input)
        obj.state_id = state_id
        storage.new(obj)
        storage.save()
        city_obj = obj.to_dict()
        return jsonify(city_obj), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update a City object. Raise 404 error if city_id
    is not linked to a City object, 400 if the request body
    is not valid JSON data. Return City dictionary with
    status code 200 otherwise.
    """
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    obj = storage.get(City, city_id)
    for k, v in user_input.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
