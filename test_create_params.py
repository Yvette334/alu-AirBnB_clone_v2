#!/usr/bin/python3
"""Test create with parameters"""

import os
import sys
from io import StringIO
from unittest.mock import patch

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from console import HBNBCommand
from models import storage

def test_create_state_with_name():
    """Test create State with name parameter"""
    console = HBNBCommand()
    storage._FileStorage__objects = {}
    
    print("Testing: create State name=\"California\"")
    
    with patch('sys.stdout', new=StringIO()) as f:
        console.onecmd('create State name="California"')
        state_id = f.getvalue().strip()
    
    print(f"Created State ID: {state_id}")
    
    # Check if state exists and has name
    key = f"State.{state_id}"
    if key in storage.all():
        state_obj = storage.all()[key]
        print(f"State found: {state_obj}")
        print(f"State name: {getattr(state_obj, 'name', 'NOT SET')}")
        
        # Test show command
        with patch('sys.stdout', new=StringIO()) as f:
            console.onecmd(f'show State {state_id}')
            show_output = f.getvalue().strip()
        print(f"Show output: {show_output}")
        
        # Check if name is in the show output
        if 'California' in show_output:
            print("✓ SUCCESS: Name parameter correctly set and displayed")
        else:
            print("✗ FAIL: Name parameter not found in show output")
    else:
        print("✗ FAIL: State not found in storage")

def test_create_place_with_multiple_params():
    """Test create Place with multiple parameters"""
    console = HBNBCommand()
    storage._FileStorage__objects = {}
    
    print("\nTesting: create Place with multiple parameters")
    
    cmd = ('create Place city_id="0001" user_id="0001" name="My_little_house" '
           'number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 '
           'latitude=37.773972 longitude=-122.431297')
    
    with patch('sys.stdout', new=StringIO()) as f:
        console.onecmd(cmd)
        place_id = f.getvalue().strip()
    
    print(f"Created Place ID: {place_id}")
    
    # Check if place exists and has all parameters
    key = f"Place.{place_id}"
    if key in storage.all():
        place_obj = storage.all()[key]
        print(f"Place found: {place_obj}")
        
        # Check specific attributes
        expected_attrs = {
            'city_id': '0001',
            'user_id': '0001', 
            'name': 'My little house',  # underscores should become spaces
            'number_rooms': 4,
            'number_bathrooms': 2,
            'max_guest': 10,
            'price_by_night': 300,
            'latitude': 37.773972,
            'longitude': -122.431297
        }
        
        all_correct = True
        for attr, expected_value in expected_attrs.items():
            actual_value = getattr(place_obj, attr, 'NOT SET')
            if actual_value == expected_value:
                print(f"✓ {attr}: {actual_value}")
            else:
                print(f"✗ {attr}: expected {expected_value}, got {actual_value}")
                all_correct = False
        
        if all_correct:
            print("✓ SUCCESS: All parameters correctly set")
        else:
            print("✗ FAIL: Some parameters incorrect")
    else:
        print("✗ FAIL: Place not found in storage")

if __name__ == '__main__':
    test_create_state_with_name()
    test_create_place_with_multiple_params()
