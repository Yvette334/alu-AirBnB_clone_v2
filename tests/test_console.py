#!/usr/bin/python3
"""Test module for console create command with parameters"""
import unittest
import os
import json
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place


class TestConsoleCreate(unittest.TestCase):
    """Test cases for the enhanced create command"""

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        # Clear storage
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up after tests"""
        # Remove test file if it exists
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_create_with_string_parameter(self):
        """Test create command with string parameter"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            state_id = f.getvalue().strip()
            
        # Verify the state was created with correct name
        key = f"State.{state_id}"
        self.assertIn(key, storage.all())
        state = storage.all()[key]
        self.assertEqual(state.name, "California")

    def test_create_with_string_underscores(self):
        """Test create command with string containing underscores"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create Place name="My_little_house"')
            place_id = f.getvalue().strip()
            
        # Verify underscores were replaced with spaces
        key = f"Place.{place_id}"
        place = storage.all()[key]
        self.assertEqual(place.name, "My little house")

    def test_create_with_escaped_quotes(self):
        """Test create command with escaped quotes in string"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="The \\"Golden\\" State"')
            state_id = f.getvalue().strip()
            
        # Verify escaped quotes were handled correctly
        key = f"State.{state_id}"
        state = storage.all()[key]
        self.assertEqual(state.name, 'The "Golden" State')

    def test_create_with_integer_parameter(self):
        """Test create command with integer parameter"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create Place number_rooms=4')
            place_id = f.getvalue().strip()
            
        # Verify integer was parsed correctly
        key = f"Place.{place_id}"
        place = storage.all()[key]
        self.assertEqual(place.number_rooms, 4)
        self.assertIsInstance(place.number_rooms, int)

    def test_create_with_float_parameter(self):
        """Test create command with float parameter"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create Place latitude=37.773972')
            place_id = f.getvalue().strip()
            
        # Verify float was parsed correctly
        key = f"Place.{place_id}"
        place = storage.all()[key]
        self.assertEqual(place.latitude, 37.773972)
        self.assertIsInstance(place.latitude, float)

    def test_create_with_multiple_parameters(self):
        """Test create command with multiple parameters"""
        cmd = ('create Place city_id="0001" user_id="0001" name="My_little_house" '
               'number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 '
               'latitude=37.773972 longitude=-122.431297')
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(cmd)
            place_id = f.getvalue().strip()
            
        # Verify all parameters were set correctly
        key = f"Place.{place_id}"
        place = storage.all()[key]
        
        self.assertEqual(place.city_id, "0001")
        self.assertEqual(place.user_id, "0001")
        self.assertEqual(place.name, "My little house")
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 10)
        self.assertEqual(place.price_by_night, 300)
        self.assertEqual(place.latitude, 37.773972)
        self.assertEqual(place.longitude, -122.431297)

    def test_create_with_invalid_parameters(self):
        """Test create command skips invalid parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California" invalid_param bad=param=value')
            state_id = f.getvalue().strip()
            
        # Verify valid parameter was set, invalid ones were skipped
        key = f"State.{state_id}"
        state = storage.all()[key]
        self.assertEqual(state.name, "California")
        self.assertFalse(hasattr(state, "invalid_param"))
        self.assertFalse(hasattr(state, "bad"))

    def test_create_without_parameters(self):
        """Test create command still works without parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State')
            state_id = f.getvalue().strip()
            
        # Verify state was created
        key = f"State.{state_id}"
        self.assertIn(key, storage.all())

    def test_create_nonexistent_class(self):
        """Test create command with nonexistent class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create NonExistentClass name="test"')
            output = f.getvalue().strip()
            
        self.assertEqual(output, "** class doesn't exist **")

    def test_create_missing_class_name(self):
        """Test create command without class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create')
            output = f.getvalue().strip()
            
        self.assertEqual(output, "** class name missing **")

    def test_parameter_parsing_edge_cases(self):
        """Test edge cases in parameter parsing"""
        console = HBNBCommand()
        
        # Test empty string
        self.assertEqual(console._parse_parameter_value('""'), "")
        
        # Test string with only underscores
        self.assertEqual(console._parse_parameter_value('"___"'), "   ")
        
        # Test invalid float
        self.assertIsNone(console._parse_parameter_value('12.34.56'))
        
        # Test invalid integer
        self.assertIsNone(console._parse_parameter_value('abc'))
        
        # Test zero values
        self.assertEqual(console._parse_parameter_value('0'), 0)
        self.assertEqual(console._parse_parameter_value('0.0'), 0.0)


if __name__ == '__main__':
    unittest.main()

