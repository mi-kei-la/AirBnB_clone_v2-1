#!/usr/bin/python3
"""Index file to test the status of the API.
Routes:
    /status [GET] - Return status of the API
    /stats [GET] - Retrieve the number of objects per type.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def return_status():
    """Return status in JSON format."""
    return jsonify(status='OK')


@app_views.route('/stats')
def return_stats():
    """Retrieve the amount of objects from each type."""
    classes = {"amenity": Amenity, "city": City,
               "place": Place, "review": Review,
               "state": State, "user": User}

    stats = {}
    for name, clss in classes.items():
        total = storage.count(clss)
        stats[name] = total
    return jsonify(stats)
