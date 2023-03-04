from ..app import db, app
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
    JSON,
    Float
)


class Location(db.Model):
    """ 
    A table for locations
    """
    __table_name__ = 'location'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    avg_temp = Column(Float)
    median_temp = Column(Float)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    
    weather = db.relationship('Forecast', backref='forecasts')
    
    def __repr__(self):
        return f'{self.name}'

class Forecast(db.Model):
    """ 
    A table for collected weather data
    """
    __table_name__ = 'forecast'
    id = Column(Integer, primary_key=True)
    period = Column(DateTime(timezone=True), server_default=func.now())
    min_temp = Column(Float)
    max_temp = Column(Float)
    humidity = Column(Float)
    location_id = Column(Integer, ForeignKey('location.id'))
    
    def __repr__(self):
        return f"Temperature for {self.location_id}"
    
    
    