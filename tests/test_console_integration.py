#!/usr/bin/python3
"""Integration tests for console create command"""
import unittest
import os
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage


class TestConsoleIntegration(unittest.TestCase):
    """Integration tests for the console create functionality"""

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        # Clear storage
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_create_and_show_with_parameters(self):
        """Test creating object with parameters and showing it"""
        # Create a state with parameters
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            state_id = f.getvalue().strip()

        # Show the created state
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'show State {state_id}')
            output = f.getvalue().strip()

        # Verify the state shows with correct name
        self.assertIn("California", output)
        self.assertIn(state_id, output)

    def test_create_and_all_with_parameters(self):
        """Test creating objects with parameters and listing them"""
        # Create multiple states
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            self.console.onecmd('create State name="Arizona"')

        # List all states
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('all State')
            output = f.getvalue().strip()

        # Verify both states are listed with correct names
        self.assertIn("California", output)
        self.assertIn("Arizona", output)

    def test_file_storage_persistence(self):
        """Test that created objects with parameters persist in file storage"""
        # Create a place with multiple parameters
        cmd = ('create Place name="Test_House" number_rooms=3 '
               'latitude=40.7128 longitude=-74.0060')
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(cmd)
            place_id = f.getvalue().strip()

        # Force save to file
        storage.save()

        # Verify file was created and contains our data
        self.assertTrue(os.path.exists("file.json"))
        
        with open("file.json", "r") as f:
            data = f.read()
            self.assertIn(place_id, data)
            self.assertIn("Test House", data)  # Underscores should be spaces
            self.assertIn("40.7128", data)

    def test_example_from_requirements(self):
        """Test the exact example from the requirements"""
        commands = [
            'create State name="California"',
            'create State name="Arizona"',
            'all State',
            ('create Place city_id="0001" user_id="0001" name="My_little_house" '
             'number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 '
             'latitude=37.773972 longitude=-122.431297'),
            'all Place'
        ]

        outputs = []
        for cmd in commands:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(cmd)
                outputs.append(f.getvalue().strip())

        # Verify states were created
        self.assertTrue(outputs[0])  # California state ID
        self.assertTrue(outputs[1])  # Arizona state ID

        # Verify states are listed correctly
        self.assertIn("California", outputs[2])
        self.assertIn("Arizona", outputs[2])

        # Verify place was created
        self.assertTrue(outputs[3])  # Place ID

        # Verify place has correct attributes
        place_output = outputs[4]
        self.assertIn("My little house", place_output)  # Underscores replaced
        self.assertIn("number_rooms': 4", place_output)
        self.assertIn("latitude': 37.773972", place_output)
        self.assertIn("longitude': -122.431297", place_output)


if __name__ == '__main__':
    unittest.main()

