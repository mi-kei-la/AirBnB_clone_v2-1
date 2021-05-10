#!/usr/bin/python3
""" This module handles all views of User objects.
"""
from models import storage
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models.base_model import BaseModel
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def ret_all_ams():
    """Retrieve a list of all Amenity object dictionaries"""
    all_ams = []
    for obj in storage.all(Amenity).values():
        all_ams.append(obj.to_dict())
    return jsonify(all_ams)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def ret_am(amenity_id):
    """Retrieve a specific amenity dictionary.
    Raise 404 error if amenity_id is not linked to an Amenity object.
    """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a specific amenity from storage.
    Raise 404 error if amenity_id is not linked to an Amenity object,
    otherwise return an empty dictionary with status code 200.
    """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """Create a new Amenity object and add to storage.
    Raise error 400 if request body is not JSON format,
    or if no name is given. Return the new Amenity with
    status code 201.
    """
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    elif user_input.get('name') is None:
        abort(400, {'message': 'Missing name'})
    else:
        obj = Amenity(**user_input)
        storage.new(obj)
        storage.save()
        state_obj = obj.to_dict()
        return jsonify(state_obj), 201
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update an Amenity object. Raise 404 error if amenity_id
    is not linked to an amenity object, 400 if the request body
    is not valid JSON data. Return Amenity dictionary with
    status code 200 otherwise.
    """
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    obj = storage.get(Amenity, amenity_id)
    for k, v in user_input.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
