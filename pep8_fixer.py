#!/usr/bin/env python3
"""
PEP8 Style Fixer for AirBnB v2 Project
This script demonstrates how to fix common PEP8 violations
"""

import re
import os

class PEP8Fixer:
    """Utility class to fix common PEP8 violations"""
    
    def __init__(self):
        self.fixes_applied = 0
    
    def fix_blank_line_whitespace(self, content):
        """Fix W293: blank line contains whitespace"""
        # Remove whitespace from blank lines
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            if line.strip() == '':  # If line is empty or only whitespace
                fixed_lines.append('')  # Replace with truly empty line
            else:
                fixed_lines.append(line)
        
        self.fixes_applied += 1
        return '\n'.join(fixed_lines)
    
    def fix_trailing_whitespace(self, content):
        """Fix W291: trailing whitespace"""
        lines = content.split('\n')
        fixed_lines = [line.rstrip() for line in lines]
        self.fixes_applied += 1
        return '\n'.join(fixed_lines)
    
    def fix_long_lines(self, content, max_length=79):
        """Fix E501: line too long"""
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            if len(line) <= max_length:
                fixed_lines.append(line)
            else:
                # Example of how to break long lines
                if '=' in line and 'def ' not in line:
                    # Break assignment lines
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        var_part = parts[0].strip()
                        value_part = parts[1].strip()
                        indent = len(line) - len(line.lstrip())
                        
                        fixed_lines.append(f"{' ' * indent}{var_part} = (")
                        fixed_lines.append(f"{' ' * (indent + 4)}{value_part}")
                        fixed_lines.append(f"{' ' * indent})")
                        continue
                
                # For other long lines, add a comment suggesting manual fix
                fixed_lines.append(line)  # Keep original, needs manual fix
        
        return '\n'.join(fixed_lines)
    
    def demonstrate_fixes(self):
        """Demonstrate common PEP8 fixes"""
        print("=== PEP8 FIXES DEMONSTRATION ===\n")
        
        # Example 1: Blank line with whitespace (W293)
        print("1. FIXING W293 - Blank line contains whitespace:")
        bad_code = "def function():\n    pass\n    \n    return True"
        print("BEFORE:")
        print(repr(bad_code))
        
        fixed_code = self.fix_blank_line_whitespace(bad_code)
        print("AFTER:")
        print(repr(fixed_code))
        print()
        
        # Example 2: Trailing whitespace (W291)
        print("2. FIXING W291 - Trailing whitespace:")
        bad_code = "def function():    \n    return True  "
        print("BEFORE:")
        print(repr(bad_code))
        
        fixed_code = self.fix_trailing_whitespace(bad_code)
        print("AFTER:")
        print(repr(fixed_code))
        print()
        
        # Example 3: Line too long (E501)
        print("3. FIXING E501 - Line too long:")
        bad_code = "very_long_variable_name = some_very_long_function_call_with_many_parameters(param1, param2, param3)"
        print("BEFORE:")
        print(f"Length: {len(bad_code)} characters")
        print(bad_code)
        
        # Manual fix example
        good_code = ("very_long_variable_name = (\n"
                    "    some_very_long_function_call_with_many_parameters(\n"
                    "        param1, param2, param3\n"
                    "    )\n"
                    ")")
        print("AFTER:")
        print(good_code)
        print()

# Specific fixes for your console.py errors
class ConsolePEP8Fixes:
    """Specific fixes for console.py"""
    
    @staticmethod
    def show_console_fixes():
        print("=== CONSOLE.PY SPECIFIC FIXES ===\n")
        
        print("1. Fix continuation line indentation (E128):")
        print("BEFORE:")
        print('    print("This is a very long line that needs to be"')
        print('+ " continued on the next line")')
        
        print("\nAFTER:")
        print('    print("This is a very long line that needs to be"')
        print('          " continued on the next line")')
        print()
        
        print("2. Fix long lines in console commands:")
        print("BEFORE:")
        print('if class_name in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:')
        
        print("\nAFTER:")
        print('valid_classes = ["BaseModel", "User", "State", "City",')
        print('                 "Amenity", "Place", "Review"]')
        print('if class_name in valid_classes:')

# Database error fix
class DatabaseErrorFixes:
    """Fixes for database integrity errors"""
    
    @staticmethod
    def show_database_fixes():
        print("=== DATABASE ERROR FIXES ===\n")
        
        print("1. Fix 'Column name cannot be null' error:")
        print("PROBLEM: create State command without required name parameter")
        print()
        
        print("CONSOLE.PY - do_create method fix:")
        print("""
def do_create(self, arg):
    '''Create a new instance of BaseModel'''
    if not arg:
        print("** class name missing **")
        return
    
    args = arg.split()
    class_name = args[0]
    
    if class_name not in self.classes:
        print("** class doesn't exist **")
        return
    
    # Parse parameters for database models
    kwargs = {}
    for param in args[1:]:
        if '=' in param:
            key, value = param.split('=', 1)
            # Handle string values
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace('_', ' ')
            # Handle numeric values
            elif '.' in value:
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:
                try:
                    value = int(value)
                except ValueError:
                    continue
            kwargs[key] = value
    
    # Create instance with parameters
    new_instance = self.classes[class_name](**kwargs)
    new_instance.save()
    print(new_instance.id)
        """)
        
        print("\nTEST FIX - Update test to include required parameters:")
        print('self.console.onecmd("create State name=\\"California\\"")')

if __name__ == '__main__':
    # Run demonstrations
    fixer = PEP8Fixer()
    fixer.demonstrate_fixes()
    
    console_fixes = ConsolePEP8Fixes()
    console_fixes.show_console_fixes()
    
    db_fixes = DatabaseErrorFixes()
    db_fixes.show_database_fixes()
    
    print(f"\nTotal fixes demonstrated: {fixer.fixes_applied}")