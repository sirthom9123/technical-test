from . import *  # noqa
from ..app import app
from datastories.models.edge import *

def seed_db(db):
    """ Add seed entities to the database. """
    with app.app_context():

        for x in User.create_defaults():
            db.session.add(x)

        db.session.commit()
