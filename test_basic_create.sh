#!/bin/bash
# Basic test script for create functionality

echo "Testing basic create State..."
echo "create State" | python3 console.py

echo -e "\nTesting create State with name..."
echo 'create State name="California"' | python3 console.py

echo -e "\nTesting create with multiple parameters..."
echo 'create Place name="My_house" number_rooms=4 latitude=37.7749 longitude=-122.4194' | python3 console.py

echo -e "\nTest completed!"
