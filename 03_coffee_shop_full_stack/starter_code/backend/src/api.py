from .database.models import db_drop_and_create_all, setup_db, Drink
from flask import Flask, request, jsonify, abort
from .auth.auth import AuthError, requires_auth
from flask_cors import CORS
from sqlalchemy import exc
import json
import os

# create and configure the app
app = Flask(__name__)
setup_db(app)
CORS(app)
'''
     @TODO uncomment the following line to initialize the datbase
     !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
     !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()


## ROUTES
'''
@TODO implement endpoint
     GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
     #get drinks
     try:
         all_drinks = Drink.query.all()
         drinks = [drink.short() for drink in all_drinks]
         return jsonify({"success": True, "drinks": drinks})
     except:
         abort(422)


'''
@TODO implement endpoint
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        all_drinks = Drink.query.order_by(Drink.id).all()
        drinks = [drink.long() for drink in all_drinks]
        return jsonify({"success": True, "drinks": drinks}), 200
    except:
        abort(422)


'''
     @TODO implement endpoint
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if title is None or recipe is None:
        abort(400)

    try:
        new_drink = Drink(title = title, recipe = json.dumps(recipe))
        new_drink.insert()
        drink = [new_drink.long()]
        return jsonify({"success": True, "drinks": drink}), 201
    except:
        abort(422)


'''
     @TODO implement endpoint
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
'''

'''
     @TODO implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
'''
## Error Handling
'''
     Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                 jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

'''

'''
@TODO implement error handler for 404
error handler should conform to general task above
'''
'''
@TODO implement error handler for AuthError
error handler should conform to general task above
'''
