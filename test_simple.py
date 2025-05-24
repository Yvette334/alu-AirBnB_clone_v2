#!/usr/bin/python3
"""Simple test to verify console functionality"""

import os
import sys
from io import StringIO
from unittest.mock import patch

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from console import HBNBCommand
from models import storage

def test_basic_create():
    """Test basic create functionality"""
    console = HBNBCommand()
    
    # Clear storage
    storage._FileStorage__objects = {}
    
    print("Testing basic create State...")
    with patch('sys.stdout', new=StringIO()) as f:
        console.onecmd("create State")
        state_id = f.getvalue().strip()
    
    print(f"Created State ID: {state_id}")
    
    # Check if state exists in storage
    key = f"State.{state_id}"
    if key in storage.all():
        print("✓ State found in storage")
        state_obj = storage.all()[key]
        print(f"State object: {state_obj}")
    else:
        print("✗ State NOT found in storage")
        print(f"Available objects: {list(storage.all().keys())}")

def test_create_with_params():
    """Test create with parameters"""
    console = HBNBCommand()
    
    # Clear storage
    storage._FileStorage__objects = {}
    
    print("\nTesting create State with name parameter...")
    with patch('sys.stdout', new=StringIO()) as f:
        console.onecmd('create State name="California"')
        state_id = f.getvalue().strip()
    
    print(f"Created State ID: {state_id}")
    
    # Check if state exists and has name
    key = f"State.{state_id}"
    if key in storage.all():
        print("✓ State found in storage")
        state_obj = storage.all()[key]
        print(f"State object: {state_obj}")
        if hasattr(state_obj, 'name'):
            print(f"State name: {state_obj.name}")
        else:
            print("✗ State has no name attribute")
    else:
        print("✗ State NOT found in storage")

def test_show_command():
    """Test show command"""
    console = HBNBCommand()
    
    # Clear storage
    storage._FileStorage__objects = {}
    
    print("\nTesting create + show...")
    
    # Create state
    with patch('sys.stdout', new=StringIO()) as f:
        console.onecmd('create State name="California"')
        state_id = f.getvalue().strip()
    
    print(f"Created State ID: {state_id}")
    
    # Show state
    with patch('sys.stdout', new=StringIO()) as f:
        console.onecmd(f'show State {state_id}')
        output = f.getvalue().strip()
    
    print(f"Show output: {output}")

if __name__ == '__main__':
    test_basic_create()
    test_create_with_params()
    test_show_command()
