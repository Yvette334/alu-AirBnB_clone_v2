#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class Amenity(BaseModel, Base):
    """Amenity model of hbnb project"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    
    # For DBStorage: Many-to-Many relationship with Place
    place_amenities = relationship("Place", secondary="place_amenity")
    
    def __init__(self, *args, **kwargs):
        """Initializes Amenity"""
        super().__init__(*args, **kwargs)
