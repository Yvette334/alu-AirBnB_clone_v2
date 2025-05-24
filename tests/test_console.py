#!/usr/bin/python3
"""Test Console"""
import unittest
import os
import sys
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place


class TestConsole(unittest.TestCase):
    """Test the console"""

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_create_state(self):
        """Test create State command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State")
            state_id = f.getvalue().strip()
        
        # Verify state was created and ID was returned
        self.assertTrue(state_id)
        key = f"State.{state_id}"
        self.assertIn(key, storage.all())

    def test_create_state_with_name(self):
        """Test create State with name parameter"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            state_id = f.getvalue().strip()
        
        # Verify state was created with correct name
        key = f"State.{state_id}"
        self.assertIn(key, storage.all())
        state = storage.all()[key]
        self.assertEqual(state.name, "California")

    def test_show_state(self):
        """Test show State command"""
        # First create a state
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State")
            state_id = f.getvalue().strip()
        
        # Then show it
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show State {state_id}")
            output = f.getvalue().strip()
        
        self.assertIn(state_id, output)
        self.assertIn("State", output)

    def test_create_city_with_state_id(self):
        """Test create City with state_id parameter"""
        # First create a state
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            state_id = f.getvalue().strip()
        
        # Then create a city with that state_id
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'create City state_id="{state_id}" name="Fremont"')
            city_id = f.getvalue().strip()
        
        # Verify city was created correctly
        key = f"City.{city_id}"
        self.assertIn(key, storage.all())
        city = storage.all()[key]
        self.assertEqual(city.state_id, state_id)
        self.assertEqual(city.name, "Fremont")

    def test_create_place_with_multiple_params(self):
        """Test create Place with multiple parameters"""
        # Create dependencies first
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            state_id = f.getvalue().strip()
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'create City state_id="{state_id}" name="San Francisco"')
            city_id = f.getvalue().strip()
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create User email="test@test.com" password="pwd" first_name="John" last_name="Doe"')
            user_id = f.getvalue().strip()
        
        # Create place with multiple parameters
        cmd = (f'create Place city_id="{city_id}" user_id="{user_id}" '
               'name="My_house" description="Beautiful_house" '
               'number_rooms=4 number_bathrooms=2 max_guest=8 '
               'price_by_night=120 latitude=37.7749 longitude=-122.4194')
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(cmd)
            place_id = f.getvalue().strip()
        
        # Verify place was created correctly
        key = f"Place.{place_id}"
        self.assertIn(key, storage.all())
        place = storage.all()[key]
        
        self.assertEqual(place.city_id, city_id)
        self.assertEqual(place.user_id, user_id)
        self.assertEqual(place.name, "My house")  # Underscores replaced
        self.assertEqual(place.description, "Beautiful house")
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 8)
        self.assertEqual(place.price_by_night, 120)
        self.assertEqual(place.latitude, 37.7749)
        self.assertEqual(place.longitude, -122.4194)

    def test_negative_values(self):
        """Test handling of negative values"""
        cmd = ('create Place number_bathrooms=0 max_guest=-3 '
               'latitude=-120.12 longitude=0.41921928')
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(cmd)
            place_id = f.getvalue().strip()
        
        key = f"Place.{place_id}"
        place = storage.all()[key]
        
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, -3)
        self.assertEqual(place.latitude, -120.12)
        self.assertEqual(place.longitude, 0.41921928)


if __name__ == '__main__':
    unittest.main()
