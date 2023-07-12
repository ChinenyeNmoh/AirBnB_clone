#!/usr/bin/env python3
import cmd
from models.base_model import BaseModel
from models import storage
import json


class HBNBCommand(cmd.Cmd):
    """create a simple console"""
    prompt = '(hbnb)'
     
    def do_quit(self, line):
        """Quit command to exit the program"""
        print("Good Bye!")
        return True

    def do_EOF(self, line):
        """Exit the program with EOF (Ctrl+D)"""
        print("")
        return True

    def help_quit(self):
        """when two statement involve"""
        print('\n'.join(["Quit command to exit the program"]))

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_create(self, line):
        """create a new instance"""
        if not line:
           print("** class name missing **")
        else:
            try:
                 new_i = eval(line)()
                 new_i.save()
                 print(new_i.id)
            except NameError:
                 print("** class doesn't exist **")
     
    def do_show(self, line):
        """Prints the string representation of an instance"""
        args = line.split()
        if not args:
            print("** class name missing **")
        else:
            try:
                cls_name = args[0]
                if cls_name not in storage.classes():
                    print("** class doesn't exist **")
                elif len(args) < 2:
                    print("** instance id missing **")
                else:
                    instance_id = args[1]
                    key = "{}.{}".format(cls_name, instance_id)
                    if key in storage.all():
                        print(storage.all()[key])
                    else:
                        print("** no instance found **")
            except Exception:
                pass

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
        args = line.split()
        if not args:
            print("** class name missing **")
        else:
            try:
                cls_name = args[0]
                if cls_name not in storage.classes():
                    print("** class doesn't exist **")
                elif len(args) < 2:
                    print("** instance id missing **")
                else:
                    instance_id = args[1]
                    key = "{}.{}".format(cls_name, instance_id)
                    if key in storage.all():
                        del storage.all()[key]
                        storage.save()
                    else:
                        print("** no instance found **")
            except Exception:
                pass

    def do_all(self, line):
        """Prints all string representations of instances"""
        args = line.split()
        obj_list = []
        if not args:
            for key in storage.all().keys():
                obj_list.append(str(storage.all()[key]))
        else:
            try:
                cls_name = args[0]
                if cls_name not in storage.classes():
                    print("** class doesn't exist **")
                else:
                    for key in storage.all().keys():
                        if key.split('.')[0] == cls_name:
                            obj_list.append(str(storage.all()[key]))
            except Exception:
                pass
        print(obj_list)

    def do_update(self, line):
        """Updates an instance based on the class name and id"""
        args = line.split()
        if not args:
            print("** class name missing **")
        else:
            try:
                cls_name = args[0]
                if cls_name not in storage.classes():
                    print("** class doesn't exist **")
                elif len(args) < 2:
                    print("** instance id missing **")
                else:
                    instance_id = args[1]
                    key = "{}.{}".format(cls_name, instance_id)
                    if key in storage.all():
                        if len(args) < 3:
                            print("** attribute name missing **")
                        elif len(args) < 4:
                            print("** value missing **")
                        else:
                            attribute_name = args[2]
                            attribute_value = args[3].strip('"')
                            obj = storage.all()[key]
                            setattr(obj, attribute_name, attribute_value)
                            obj.save()
                    else:
                        print("** no instance found **")
            except Exception:
                pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
