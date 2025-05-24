#!/usr/bin/python3
"""Console Module for AirBnB Clone"""
import cmd
import re
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB clone"""
    
    prompt = "(hbnb) "
    
    # Dictionary of available classes
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing when empty line is entered"""
        pass

    def do_create(self, arg):
        """Create a new instance of a class with optional parameters
        
        Usage: create <Class name> <param 1> <param 2> <param 3>...
        Param syntax: <key name>=<value>
        
        Value types:
        - String: "value" (quotes required, underscores become spaces)
        - Float: number.decimal (contains dot)
        - Integer: number (default case)
        """
        if not arg:
            print("** class name missing **")
            return

        # Split arguments while preserving quoted strings
        try:
            args = shlex.split(arg)
        except ValueError:
            # If shlex fails, fall back to simple split but handle quotes manually
            args = []
            current_arg = ""
            in_quotes = False
            i = 0
            while i < len(arg):
                char = arg[i]
                if char == '"' and (i == 0 or arg[i-1] != '\\'):
                    in_quotes = not in_quotes
                    current_arg += char
                elif char == ' ' and not in_quotes:
                    if current_arg:
                        args.append(current_arg)
                        current_arg = ""
                else:
                    current_arg += char
                i += 1
            if current_arg:
                args.append(current_arg)

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        # Create new instance
        new_instance = self.classes[class_name]()
        
        # Process parameters if any
        if len(args) > 1:
            for param in args[1:]:
                if '=' not in param:
                    continue  # Skip invalid parameters
                
                try:
                    key, value = param.split('=', 1)
                    
                    # Skip if key is empty
                    if not key:
                        continue
                    
                    # Parse value based on type
                    parsed_value = self._parse_parameter_value(value)
                    
                    # Skip if parsing failed
                    if parsed_value is None:
                        continue
                    
                    # Set attribute on the instance
                    setattr(new_instance, key, parsed_value)
                
            except ValueError:
                # Skip parameters that can't be split properly
                continue
    
    # Save the instance
    new_instance.save()
    print(new_instance.id)

    def _parse_parameter_value(self, value):
        """Parse parameter value and return appropriate Python type
        
        Args:
            value (str): The value string to parse
            
        Returns:
            Parsed value or None if parsing fails
        """
        # String value (starts and ends with quotes)
        if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
            # Remove quotes and process escapes
            string_value = value[1:-1]
            # Replace escaped quotes
            string_value = string_value.replace('\\"', '"')
            # Replace underscores with spaces
            string_value = string_value.replace('_', ' ')
            return string_value
        
        # Float value (contains a dot)
        elif '.' in value:
            try:
                return float(value)
            except ValueError:
                return None
        
        # Integer value (numeric, including negative)
        else:
            try:
                return int(value)
            except ValueError:
                return None

    def do_show(self, arg):
        """Show an instance based on class name and id"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        print(storage.all()[key])

    def do_destroy(self, arg):
        """Delete an instance based on class name and id"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Show all instances or all instances of a specific class"""
        objects = storage.all()
        
        if not arg:
            # Show all objects
            print([str(obj) for obj in objects.values()])
        else:
            # Show objects of specific class
            if arg not in self.classes:
                print("** class doesn't exist **")
                return
            
            filtered_objects = [str(obj) for key, obj in objects.items() 
                              if key.startswith(arg + ".")]
            print(filtered_objects)

    def do_update(self, arg):
        """Update an instance based on class name, id, attribute name and value"""
        if not arg:
            print("** class name missing **")
            return

        args = shlex.split(arg)
        
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3]

        # Try to cast the value to the appropriate type
        if hasattr(obj, attr_name):
            attr_type = type(getattr(obj, attr_name))
            try:
                attr_value = attr_type(attr_value)
            except (ValueError, TypeError):
                pass

        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
