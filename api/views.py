from flask import Blueprint, jsonify, request

import utils
from database import db
from login import models as login_models

api_view = Blueprint('api_view', __name__)


@api_view.route('/users/')
@utils.login_required
def users():
    return jsonify([user.serialize() for user in login_models.User.query.all()])


@api_view.route('/users/', methods=['POST'])
@utils.login_required
@utils.permission_required('full_access')
def user_create():
    user = login_models.User(
        username=request.form.get('username'),
        password=utils.hash_password(request.form.get('password')),
        role_id=request.form.get('role_id'),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201


@api_view.route('/users/<int:user_id>/')
@utils.login_required
def user_get(user_id: int):
    user = login_models.User.query.get_or_404(user_id)
    return jsonify(user.serialize())


@api_view.route('/users/<int:user_id>/', methods=['PUT'])
@utils.login_required
@utils.permission_required('full_access')
def user_update(user_id: int):
    user = login_models.User.query.get_or_404(user_id)
    user.username = request.form.get('username')
    password = request.form.get('password')
    if password is not None and len(password) > 0:
        user.password = utils.hash_password(password)
    user.role_id = request.form.get('role_id')
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())


@api_view.route('/users/<int:user_id>/', methods=['DELETE'])
@utils.login_required
@utils.permission_required('full_access')
def user_delete(user_id: int):
    user = login_models.User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})


@api_view.route('/roles/')
@utils.login_required
def roles():
    return jsonify([role.serialize() for role in login_models.Role.query.all()])
