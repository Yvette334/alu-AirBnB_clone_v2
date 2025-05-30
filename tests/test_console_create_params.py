#!/usr/bin/python3
"""Test Console create command with parameters"""
import unittest
from unittest.mock import patch
from io import StringIO
import os
from console import HBNBCommand
import models
from models.state import State
from models.city import City
from models.place import Place
from models.user import User


class TestConsoleCreateParams(unittest.TestCase):
    """Test the console create command with parameters"""

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        models.storage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up after tests"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_create_state_with_name(self):
        """Test create State with name parameter"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            state_id = f.getvalue().strip()
        key = f"State.{state_id}"
        self.assertIn(key, models.storage.all())
        state = models.storage.all()[key]
        self.assertEqual(state.name, "California")

    def test_create_state_underscore_to_space(self):
        """Test create State with underscores converted to spaces"""
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create State name="San_Francisco_is_super_cool"'
            self.console.onecmd(cmd)
            state_id = f.getvalue().strip()
        key = f"State.{state_id}"
        state = models.storage.all()[key]
        self.assertEqual(state.name, "San Francisco is super cool")

    def test_create_place_with_multiple_params(self):
        """Test create Place with multiple params"""
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = ('create Place city_id="0001" user_id="0001" '
                   'name="My_little_house" number_rooms=4 '
                   'number_bathrooms=2 max_guest=10 price_by_night=300 '
                   'latitude=37.773972 longitude=-122.431297')
            self.console.onecmd(cmd)
            place_id = f.getvalue().strip()
        key = f"Place.{place_id}"
        place = models.storage.all()[key]
        self.assertEqual(place.city_id, "0001")
        self.assertEqual(place.user_id, "0001")
        self.assertEqual(place.name, "My little house")
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 10)
        self.assertEqual(place.price_by_night, 300)
        self.assertEqual(place.latitude, 37.773972)
        self.assertEqual(place.longitude, -122.431297)

    def test_create_with_escaped_quotes(self):
        """Test create with escaped quotes in string"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California\\"s_best"')
            state_id = f.getvalue().strip()
        key = f"State.{state_id}"
        state = models.storage.all()[key]
        self.assertEqual(state.name, 'California"s best')

    def test_create_skip_invalid_params(self):
        """Test that invalid parameters are skipped"""
        with patch('sys.stdout', new=StringIO()) as f:
            cmd =  'create State name="California\\"s_best"'
            self.console.onecmd(cmd)
            state_id = f.getvalue().strip()
        key = f"State.{state_id}"
        state = models.storage.all()[key]
        self.assertEqual(state.name, "California")
        self.assertFalse(hasattr(state, 'invalid_param'))

    def test_create_negative_numbers(self):
        """Test create with negative numbers"""
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create Place max_guest=-3 latitude=-120.12'
            self.console.onecmd(cmd)
            place_id = f.getvalue().strip()
        key = f"Place.{place_id}"
        place = models.storage.all()[key]
        self.assertEqual(place.max_guest, -3)
        self.assertEqual(place.latitude, -120.12)

    def test_create_without_params(self):
        """Test create without parameters (should still work)"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State')
            state_id = f.getvalue().strip()
        key = f"State.{state_id}"
        self.assertIn(key, models.storage.all())


if __name__ == '__main__':
    unittest.main()
