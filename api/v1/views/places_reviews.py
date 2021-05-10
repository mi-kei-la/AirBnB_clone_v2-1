#!/usr/bin/python3
""" This module handles all views of Review objects.
"""
from models import storage
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieve all reviews of the place linked to a given place_id.
    Raise 404 error otherwise"""
    if storage.get(Place, place_id) is None:
        abort(404)
    review_dict = storage.all(Review)
    review_list = []
    for rev in review_dict.values():
        if rev.place_id == place_id:
            rev = rev.to_dict()
            review_list.append(rev)
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve Review object linked to a given id. Raise 404 otherwise."""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete Review from storage. If successful, return empty
    dictionary with status code 200, otherwise raise 404 error.
    """
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def add_review(place_id):
    """Create a new Review object related to the given place,
    and add to storage. Raise error 400 if request body is
    not JSON format, if no user_id is given, or if no text is given.
    Return the new Review with status code 201.
    """
    # Check that user input is correct
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    elif user_input.get('text') is None:
        abort(400, {'message': 'Missing text'})
    elif user_input.get('user_id') is None:
        abort(400, {'message': 'Missing user_id'})
    else:
        # Review is linked to user and city
        u_id = user_input.get('user_id')
        if storage.get(User, u_id) is None:
            abort(404)
        elif storage.get(Place, place_id) is None:
            abort(404)
        else:
            obj = Review(**user_input)
            obj.user_id = u_id
            obj.place_id = place_id
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Update a Review object. Raise 404 error if review_id
    is not linked to a Review, 400 if the request body
    is not valid JSON data. Return Review dictionary with
    status code 200 otherwise.
    """
    user_input = request.get_json()
    if user_input is None:
        abort(400, {'message': 'Not a JSON'})
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    for k, v in user_input.items():
        if k not in ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
