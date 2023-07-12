#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advance command syntax.
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''

        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            lines = lines[:]

            _cls = lines[:lines.find('.')]

            _cmd = lines[lines.find('.') + 1:lines.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            lines = lines[lines.find('(') + 1:lines.find(')')]
            if lines:
                lines = lines.partition(', ')

                _id = lines[0].replace('\"', '')

                lines = lines[2].strip()
                if lines:
                    if lines[0] == '{' and lines[-1] == '}'\
                            and type(eval(lines)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an blueprint of a class"""
        try:
            if not args:
                raise SyntaxError()
            arg_list = args.split(" ")
            kiwi = {}
            for arg in arg_list[1:]:
                arg_splited = arg.split("=")
                arg_splited[1] = eval(arg_splited[1])
                if type(arg_splited[1]) is str:
                    arg_splited[1] = arg_splited[1].replace("_", " ").replace('"', '\\"')
                kiwi[arg_splited[0]] = arg_splited[1]
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        new_i = HBNBCommand.classes[arg_list[0]](**kiwi)
        new_i.save()
        print(new_i.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new_args = args.partition(" ")
        _name = new_args[0]
        _id = new_args[2]

        if _id and ' ' in c_id:
            _id = _id.partition(' ')[0]

        if not _name:
            print("** class name missing **")
            return

        if _name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not _id:
            print("** instance id missing **")
            return

        key = _name + "." + _id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        _name = new[0]
        _id = new[2]
        if _id and ' ' in c_id:
            _id = _id.partition(' ')[0]

        if not _name:
            print("** class name missing **")
            return

        if _name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not _id:
            print("** instance id missing **")
            return

        key = _name + "." + _id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        _list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for key, j in storage.all(HBNBCommand.classes[args]).items():
                _list.append(str(j))
        else:
            for key, j in storage.all().items():
                _list.append(str(j))
        print(_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for key, j in storage._FileStorage__objects.items():
            if args == key.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        _name = c_id = att_name = att_val = kwargs = ''

        args = args.partition(" ")
        if args[0]:
            _name = args[0]
        else:
            print("** class name missing **")
            return
        if _name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:
            print("** instance id missing **")
            return

        key = _name + "." + c_id

        if key not in storage.all():
            print("** no instance found **")
            return

        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []
            for key, j in kwargs.items():
                args.append(key)
                args.append(j)
        else:
            args = args[2]
            if args and args[0] == '\"':
                _quote = args.find('\"', 1)
                att_name = args[1:_quote]
                args = args[_quote + 1:]

            args = args.partition(' ')

            if not att_name and args[0] != ' ':
                att_name = args[0]
            if args[2] and args[2][0] == '\"':
                at_value = args[2][1:args[2].find('\"', 1)]

            if not at_value and args[2]:
                at_value = args[2].partition(' ')[0]

            args = [att_name, at_value]

        _dict = storage.all()[key]

        for i, att_name in enumerate(args):
            if (i % 2 == 0):
                at_value = args[i + 1]
                if not att_name:
                    print("** attribute name missing **")
                    return
                if not at_value:
                    print("** value missing **")
                    return
                if att_name in HBNBCommand.types:
                    at_value = HBNBCommand.types[att_name](at_value)

                _dict.__dict__.update({att_name: at_value})

        _dict.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
