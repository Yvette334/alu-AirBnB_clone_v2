#!/usr/bin/python3
"""
Contains the City class
"""

from models.base_model import BaseModel


class City(BaseModel):
    """Representation of city"""
    state_id = ""
    name = ""
