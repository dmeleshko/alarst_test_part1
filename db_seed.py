from app import db
from login import models
import utils

if __name__ == '__main__':
    db.create_all()

    full_access_role = models.Role(
        name='full_access',
    )

    readonly_role = models.Role(
        name='readonly',
    )

    first_user = models.User(
        username='admin',
        password=utils.hash_password('admin'),
        role=full_access_role,
    )

    db.session.add(full_access_role)
    db.session.add(readonly_role)
    db.session.add(first_user)
    db.session.commit()
