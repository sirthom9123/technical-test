from . import *  # noqa
from ..app import app
from weather.models.weather_table import *

def seed_db(db):
    """ Add seed entities to the database. """
    with app.app_context():


        for x in User.create_defaults():
            db.session.add(x)

        for x in Role.create_defaults():
            db.session.add(x)
        db.session.commit()
