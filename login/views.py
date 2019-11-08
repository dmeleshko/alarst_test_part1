from flask import (
    Blueprint, session, render_template, request, flash, redirect,
    url_for, g,
)

import utils
from login import models as login_models

login_view = Blueprint('login_view', __name__)


@login_view.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@login_view.route('/login/', methods=['POST'])
def login_proceed():
    username = request.form.get('username')
    user = login_models.User.query.filter_by(username=username).first()
    if user is None:
        flash('You provided invalid credentials')
        return redirect(url_for('login_view.login'))
    password = request.form.get('password', '')
    if not utils.check_password(password, user.password):
        flash('You provided invalid credentials')
        return redirect(url_for('login_view.login'))
    session['user_id'] = user.id
    return redirect(url_for('index'))


@login_view.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))
