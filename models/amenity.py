#!/usr/bin/python3
"""
Contains the Amenity class
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class Amenity(BaseModel, Base):
    """Representation of Amenity"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    
    # For DBStorage: relationship with Place using place_amenity as secondary table
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = relationship("Place", secondary="place_amenity", viewonly=False, back_populates="amenities")
