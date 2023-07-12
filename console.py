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


if __name__ == '__main__':
    HBNBCommand().cmdloop()
