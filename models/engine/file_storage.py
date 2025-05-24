#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects or filtered by class"""
        if cls is not None:
            # Filter objects by class type
            filtered_objects = {}
            for key, obj in FileStorage.__objects.items():
                if isinstance(obj, cls):
                    filtered_objects[key] = obj
            return filtered_objects
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in FileStorage.__objects:
            json_objects[key] = FileStorage.__objects[key].to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                class_name = jo[key]["__class__"]
                if class_name == "BaseModel":
                    FileStorage.__objects[key] = BaseModel(**jo[key])
                elif class_name == "User":
                    FileStorage.__objects[key] = User(**jo[key])
                elif class_name == "State":
                    FileStorage.__objects[key] = State(**jo[key])
                elif class_name == "City":
                    FileStorage.__objects[key] = City(**jo[key])
                elif class_name == "Amenity":
                    FileStorage.__objects[key] = Amenity(**jo[key])
                elif class_name == "Place":
                    FileStorage.__objects[key] = Place(**jo[key])
                elif class_name == "Review":
                    FileStorage.__objects[key] = Review(**jo[key])
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it's inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload()
