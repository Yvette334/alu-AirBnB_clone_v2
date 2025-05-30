#!/usr/bin/python3
""" Test link Many-To-Many Place <> Amenity
"""
import os
os.environ['HBNB_TYPE_STORAGE'] = 'db'
os.environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
os.environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
os.environ['HBNB_MYSQL_HOST'] = 'localhost'
os.environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'

from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity

# creation of a State
state = State(name="California")
state.save()

# creation of a City
city = City(state_id=state.id, name="San Francisco")
city.save()

# creation of a User
user = User(email="john@snow.com", password="johnpwd")
user.save()

# creation of 2 Places
place_1 = Place(user_id=user.id, city_id=city.id, name="House 1")
place_1.save()
place_2 = Place(user_id=user.id, city_id=city.id, name="House 2")
place_2.save()

# creation of 3 various Amenity
amenity_1 = Amenity(name="Wifi")
amenity_1.save()
amenity_2 = Amenity(name="Cable")
amenity_2.save()
amenity_3 = Amenity(name="Eth")
amenity_3.save()

# link place_1 with 2 amenities
place_1.amenities.append(amenity_1)
place_1.amenities.append(amenity_2)

# link place_2 with 3 amenities
place_2.amenities.append(amenity_1)
place_2.amenities.append(amenity_2)
place_2.amenities.append(amenity_3)

storage.save()

print("OK")
