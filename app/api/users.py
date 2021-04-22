import re
from flask import request, jsonify, url_for
from app import db
from app.api import bp
# from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')

    message = {}
    if 'username' not in data or not data.get('username', None):
        message['username'] = 'Please provide a valid username.'
    if 'password' not in data or not data.get('password', None):
        message['password'] = 'Please provide a valid password.'
    if User.query.filter_by(username=data.get('username', None)).first():
        message['username'] = 'Please use a different username.'
    if message:
        return bad_request(message)

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    pass