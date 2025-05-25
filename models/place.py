#!/usr/bin/python3
"""
Contains the Place class
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# Association table for Many-to-Many relationship between Place and Amenity
place_amenity = Table('place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """Representation of Place"""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    # For DBStorage: relationship with Amenity using place_amenity as secondary table
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)

    @property
    def amenities(self):
        """Getter for amenities"""
        import models
        if models.storage_t != "db":
            amenity_list = []
            all_amenities = models.storage.all("Amenity")
            for amenity in all_amenities.values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

    @amenities.setter
    def amenities(self, obj):
        """Setter for amenities"""
        import models
        if models.storage_t != "db":
            if obj.__class__.__name__ == "Amenity":
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
