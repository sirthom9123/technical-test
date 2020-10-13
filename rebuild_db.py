from weather.models import db
# Seeds
from weather.models.seeds import seed_db

# Initialize db
db.drop_all()
db.configure_mappers()
db.create_all()

# Seeds
seed_db(db)