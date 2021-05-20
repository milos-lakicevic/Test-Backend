import json
import boto3
from flask_lambda import FlaskLambda
from flask import request, jsonify
import uuid

app = FlaskLambda(__name__)

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table('users')


@app.route('/', methods=['GET'])
def index():
    data = {
        "message": "Routing works!"
    }
    return (
        json.dumps(data),
        200,
        {'Content-Type': "application/json"}
    )


@app.route('/users', methods=['POST'])
def createUser():
    id = 'USER#' + str(uuid.uuid4())
    user = {
        'user_id': id,
        'username': request.json.get('username'),
        'first_name': request.json.get('first_name'),
        'last_name': request.json.get('last_name'),
        'email': request.json.get('email')
    }

    table.put_item(Item=user)

    return (
        json.dumps(user),
        201,
        {'Content-Type': "application/json"}
    )


@app.route('/users/<user_id>', methods=['GET'])
def getUserById(user_id):
    user = table.get_item(Key={'user_id': 'USER#' + user_id})['Item']
    return (
        json.dumps(user),
        200,
        {'Content-Type': "application/json"}
    )


@app.route('/users/<user_id>', methods=["PATCH"])
def updateUser(user_id):
    id = 'USER#' + user_id
    user = table.update_item(
        Key={
            'user_id': id
        },
        UpdateExpression="set username=:uname, first_name=:fname, last_name=:lname, email=:mail",
        ExpressionAttributeValues={
            ':uname': request.json.get('username'),
            ':fname': request.json.get('first_name'),
            ':lname': request.json.get('last_name'),
            ':mail': request.json.get('email')
        },
        ReturnValues="UPDATED_NEW"
    )
    return (
        json.dumps(user),
        200,
        {'Content-Type': "application/json"}
    )


@app.route('/users/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    table.delete_item(Key={'user_id': "USER#" + user_id})
    msg = {
        'message': 'User with ID ' + user_id + ' is deleted successfully!'
    }
    return {
        json.dumps(msg),
        200,
        {'Content-Type': "application/json"}
    }