#!/usr/bin/python3
"""Init file for all API views.
Views:
    - status [GET]
    - stats (number of objects per type) [GET]
    - State [GET/PUT/POST/DELETE]
    - City [GET/PUT/POST/DELETE]
    - Amenity [GET/PUT/POST/DELETE]
    - User [GET/PUT/POST/DELETE]
    - Place [GET/PUT/POST/DELETE]
    - Reviews [GET/PUT/POST/DELETE]

Default route prefix: /api/v1
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
