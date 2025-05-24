#!/usr/bin/python3
"""
Contains the Review class
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Representation of Review"""
    place_id = ""
    user_id = ""
    text = ""
