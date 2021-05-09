#!/usr/bin/python3
""" This module handles all views of Place objects.
"""
from models import storage
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """Retrieve all Places of the city linked to a given city_id.
    Raise 404 error otherwise"""
    if storage.get(City, city_id) is None:
        abort(404)
    place_dict = storage.all(Place)
    place_list = []
    for place in place_dict.values():
        if place.city_id == city_id:
            place = place.to_dict()
            place_list.append(place)
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve Place object linked to a given id. Raise 404 otherwise."""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete Place from storage. If successful, return empty
    dictionary with status code 200, otherwise raise 404 error.
    """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """Create a new Place object related to the given city,
    and add to storage. Raise error 400 if request body is
    not JSON format, or if no name is given.
    Return the new Place with status code 201.
    """
    # Check that user input is correct
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    elif user_input.get('name') is None:
        abort(400, {'message': 'Missing name'})
    elif user_input.get('user_id') is None:
        abort(400, {'message': 'Missing user_id'})
    else:
        # Place is linked to user and city
        u_id = user_input.get('user_id')
        if storage.get(User, u_id) is None:
            abort(404)
        elif storage.get(City, city_id) is None:
            abort(404)
        else:
            obj = Place(**user_input)
            obj.user_id = u_id
            obj.city_id = city_id
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a Place object. Raise 404 error if place_id
    is not linked to a Place object, 400 if the request body
    is not valid JSON data. Return Place dictionary with
    status code 200 otherwise.
    """
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    for k, v in user_input.items():
        if k not in ['id', 'user_id', 'city_id',
                     'created_at', 'updated_at']:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
