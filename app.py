from flask import render_template, session, g

import config
import utils
from login import models as login_models

app = utils.create_app(config)


@app.before_request
def load_user():
    if 'user_id' in session:
        g.user = login_models.User.query.get(session["user_id"])
        if not g.user:
            session.pop('user_id')
    else:
        g.user = None


@app.route('/')
@utils.login_required
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
