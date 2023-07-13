#!/usr/bin/env python3

import cmd
import re
import models
from models.base_model import BaseModel
from models import storage
import json
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class_home = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "Amenity": Amenity,
    "City": City,
    "Review": Review,
    "State": State
}


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb)  '

    def do_EOF(self, line):
        """Exits console"""
        print("")
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        print("Good Bye!")
        return True

    def help_quit(self):
        """when two arguments involve"""
        print('\n'.join(["Quit command to exit the program"]))

    def emptyline(self):
        """ overwriting the emptyline method """
        pass

    def do_create(self, line):
        """Creates a new instances of a class"""
        if line:
            try:
                _globe = globals().get(line, None)
                obj = _globe()
                obj.save()
                print(obj.id)
            except Exception:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_show(self, line):
        """print <class name> <id>"""
        arr = line.split()

        if len(arr) < 1:
            print("** class name missing **")
        elif arr[0] not in class_home:
            print("** class doesn't exist **")
        elif len(arr) < 2:
            print("** instance id missing **")
        else:
            new_s = f"{arr[0]}.{arr[1]}"
            if new_s not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[new_s])

            new_s = f"{arr[0]}.{arr[1]}"
            if new_s not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[new_s])

    def do_destroy(self, line):
        """
        Create Destroy command deletes an instance based on the class name.
        """
        arr = line.split()
        if len(arr) < 1:
            print("** class name missing **")
        elif arr[0] not in class_home:
            print("** class doesn't exist **")
        elif len(arr) < 2:
            print("** instance id missing **")
        else:
            new_str = f"{arr[0]}.{arr[1]}"
            if new_str not in storage.all().keys():
                print("** no instance found **")
            else:
                storage.all().pop(new_str)
                storage.save()

    def do_all(self, line):
        """ Print all instances in string representation """
        objects = []
        if line == "":
            print([str(value) for key, value in storage.all().items()])
        else:
            state = line.split(" ")
            if state[0] not in class_home:
                print("** class doesn't exist **")
            else:
                for key, value in storage.all().items():
                    split_class = key.split(".")
                    if split_class[0] == state[0]:
                        objects.append(str(value))
                print(objects)

    def do_update(self, line):
        """Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        usage:  update <class> <id> <attribute_name> <attribute_value> or
                <class>.update(<id>, <attribute_name>, <attribute_value>) or
                <class>.update(<id>, <dictionary>)
        """
        arrays = line.split()
        if len(arrays) < 1:
            print("** class name missing **")
            return
        elif arrays[0] not in class_home:
            print("** class doesn't exist **")
            return
        elif len(arrays) < 2:
            print("** instance id missing **")
            return
        else:
            new_string = f"{arrays[0]}.{arrays[1]}"
            if new_string not in storage.all().keys():
                print("** no instance found **")
            elif len(arrays) < 3:
                print("** attribute name missing **")
                return
            elif len(arrays) < 4:
                print("** value missing **")
                return
            else:
                setattr(storage.all()[new_string], arrays[2], arrays[3])
                storage.save()

    def do_count(self, line):
        """Print the count all class instances"""
        class_g = globals().get(line, None)
        if class_g is None:
            print("** class doesn't exist **")
            return
        count = 0
        for obj in storage.all().values():
            if obj.__class__.__name__ == line:
                count += 1
        print(count)

    def default(self, line):
        if line is None:
            return

        Pattern = r"^([A-Za-z]+)\.([a-z]+)([^(]*)\)"
        params_pattern = r"""^"([^"]+)"(?:,\s*(?:"([^"]+)"|(\{[^}]+\}))
                                (?:,\s*(?:("?[^"]+"?)))?)?"""
        same = re.match(Pattern, line)
        if not same:
            super().default(line)
            return
        Name, Method, Params = same.groups()
        same = re.match(params_pattern, Params)
        Params = [item for item in same.groups() if item] if same else []

        cmd = " ".join([Name] + Params)

        if Method == 'all':
            return self.do_all(cmd)
        elif Method == 'count':
            return self.do_count(cmd)
        elif Method == 'show':
            return self.do_show(cmd)
        elif Method == 'destroy':
            return self.do_destroy(cmd)
        elif Method == 'update':
            return self.do_update(cmd)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
