from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db, db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

"""
Initialize the database.
!! WARNING: db_drop_and_create_all() DROPS ALL RECORDS and reseeds from scratch.
Uncomment it only for a first run (or to reset); leaving it active wipes the
database on every start/reload. The repo already ships a seeded database.db, so
it stays commented by default.
"""
# db_drop_and_create_all()


def validated_recipe(recipe):
    """Serialize a recipe, rejecting anything Drink.short() cannot read.

    short() iterates the stored recipe and indexes each entry, and it backs the
    PUBLIC GET /drinks. So a recipe that is missing, not a list, or not made of
    objects would let an authorized writer break that endpoint for every
    visitor until the row is removed. Validate before it reaches the database.
    """
    if not isinstance(recipe, list) or not recipe:
        abort(400)

    for ingredient in recipe:
        if not isinstance(ingredient, dict):
            abort(400)
        if 'color' not in ingredient or 'parts' not in ingredient:
            abort(400)

    return json.dumps(recipe)


# ROUTES

"""
  GET /drinks
      public endpoint
  returns status code 200 and json {"success": True, "drinks": drinks}
  where drinks is the list of drinks
      or appropriate status code indicating reason for failure
"""


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.order_by(Drink.id).all()
    parsed_drinks = [drink.short() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': parsed_drinks
    })


"""
  GET /drinks-detail
      requires the 'get:drinks-detail' permission
  returns status code 200 and json {"success": True, "drinks": drinks}
  where drinks is the list of drinks
      or appropriate status code indicating reason for failure
"""


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(jwt):
    drinks = Drink.query.order_by(Drink.id).all()
    parsed_drinks = [drink.long() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': parsed_drinks
    })


"""
  POST /drinks
      creates a new row in the drinks table
      requires the 'post:drinks' permission
  returns status code 200 and json {"success": True, "drinks": drink}
  where drink an array containing only the newly created drink
      or appropriate status code indicating reason for failure
"""


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(jwt):
    # silent=True: a missing or non-JSON body becomes {} and is reported as a
    # 400 below, instead of raising an AttributeError and returning an
    # HTML 500.
    body = request.get_json(silent=True) or {}

    drink_title = body.get('title')

    if not drink_title:
        abort(400)

    parsed_drink_recipe = validated_recipe(body.get('recipe'))

    try:
        drink = Drink(title=drink_title, recipe=parsed_drink_recipe)
        drink.insert()
    except exc.IntegrityError:
        db.session.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


"""
  PATCH /drinks/<id>
      where <id> is the existing model id
      responds with a 404 error if <id> is not found
      updates the corresponding row for <id>
      requires the 'patch:drinks' permission
  returns status code 200 and json {"success": True, "drinks": drink}
  where drink an array containing only the updated drink
      or appropriate status code indicating reason for failure
"""


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, drink_id):
    body = request.get_json(silent=True) or {}

    if 'title' not in body and 'recipe' not in body:
        abort(400)

    if 'title' in body and not body['title']:
        abort(400)

    if 'recipe' in body:
        parsed_drink_recipe = validated_recipe(body['recipe'])

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if drink is None:
        abort(404)

    try:
        if 'title' in body:
            drink.title = body['title']

        if 'recipe' in body:
            drink.recipe = parsed_drink_recipe

        drink.update()
    except exc.IntegrityError:
        db.session.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


"""
  DELETE /drinks/<id>
      where <id> is the existing model id
      responds with a 404 error if <id> is not found
      deletes the corresponding row for <id>
      requires the 'delete:drinks' permission
  returns status code 200 and json {"success": True, "delete": id}
  where id is the id of the deleted record
      or appropriate status code indicating reason for failure
"""


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if drink is None:
        abort(404)

    try:
        drink.delete()
    except exc.IntegrityError:
        db.session.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'delete': drink.id
    })


# Error Handling
"""
Error handling for bad request
"""


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


"""
Error handling for unauthorized
"""


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


"""
Error handling for not found entity
"""


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


"""
Error handling for unprocessable entity
"""


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


"""
Error handling for an unexpected server error, so that even this case keeps the
JSON contract instead of returning Flask's HTML error page
"""


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


"""
Error handling for AuthError
"""


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
