#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel


#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# Association table for many-to-many relationship between Place and Amenity
association_table = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False, default="")
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False, default="")
    name = Column(String(128), nullable=False, default="")
    description = Column(String(1024), nullable=True, default="")
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True, default=0.0)
    longitude = Column(Float, nullable=True, default=0.0)
    
    # For FileStorage compatibility
    amenity_ids = []
    
    def __init__(self, *args, **kwargs):
        """Initializes Place"""
        super().__init__(*args, **kwargs)
