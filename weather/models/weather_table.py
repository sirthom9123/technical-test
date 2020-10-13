from ..app import db, app
from sqlalchemy.orm import relationship, configure_mappers, backref
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    Boolean,
    event,
    ARRAY,
    Date,
    Time,
    JSON
)
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable

make_searchable(db.metadata)
# configure_mappers()  # IMPORTANT!
