#!/usr/bin/python3
"""
Command intepreter to handle the commands

contains the entry point of the command interpreter
"""

import cmd
import shlex
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import models
from signal import SIGKILL
import os


class HBNBCommand(cmd.Cmd):
    """
    This class servs as a command intepretor using the cmd module
    methods:
        create: Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id

        show: Prints the string representation of an instance based
        on the class name and id

        destroy: Deletes an instance based on the class name and id
        (save the change into the JSON file)

        all: Prints all string representation of all instances
        based or not on the class name.

        update: Updates an instance based on the class name and
        id by adding or updating attribute
    """
    prompt = "(hbnb) "

    def emptyline(self):
        """Overide the emptyline method to skip emptyl line"""
        return False

    def parseline(self, line):

        dot = line.find(".")
        br = line.find("(")
        br2 = line.find(")")

        if dot != -1:
            if br != -1 and br2 != -1:
                clss = line.split(".")[0]
                cmnd = line.split(".")[1].split("(")[0]
                arg = line.split(".")[1].split("(")[1]
                if cmnd == "count":
                    objects = models.storage.all()
                    lst = []
                    if clss in classes:
                        for k in objects.keys():
                            key = k.split(".")
                            if key[0] == clss:
                                lst.append(str(objects[k]))
                        print(len(lst))
                        line = "\n"
                    else:
                        print("** class doesn't exist **")
                elif cmnd == "show" or cmnd == "destroy" or cmnd == "all":
                    line = f"{cmnd} {clss} {arg[:-1]}"
                elif cmnd == "update":
                    if arg.find("{") != -1 and arg.find("}") != -1:
                        my_dict = arg.replace('"', "").replace("'", "")
                        my_dict = my_dict.replace("{", "").replace("}", "")
                        my_dict = my_dict.replace(")", "").split(", ")
                        ids = my_dict.pop(0)
                        for ele in my_dict:
                            tri = ele.split(': ')[0]
                            value = ele.split(': ')[1]
                            s = f'{clss} {ids} "{tri}" "{value}"'
                            self.do_update(s)
                            line = "\n"
                    else:
                        arg = arg.split(",")
                        line = f"{cmnd} {clss} {arg[0]}\
                                {arg[1][1:]} {arg[2][1:-1]}"

        return cmd.Cmd.parseline(self, line)

    def do_quit(self, arg):
        """Quit command to exit the console
        """
        return True

    def do_EOF(self, arg):
        """ ctrl-d command to exit the console
        """
        print()
        return True

    def do_create(self, arg):
        """Creates a new instance of a class and print it's id
Usage: create <class name>
Arguments:
    <class name>: Name of the class
Return:
    Print the id of the newly created instance
        """
        if not serch_clss(arg):
            return False
        arg = shlex.split(arg)
        new_obj = classes[arg[0]]()
        new_obj.save()
        print(new_obj.id)

    def do_show(self, arg):
        """Prints the string representation of an instance
based on the class name and id
Usage: show <class name> <class id>
Arguments:
    <class name>: Name of the class
    <class id>: Id of the class
Return:
    Prints the object matching class name and id
"""
        key = serch_clss(arg, True)
        if key is None or not key:
            return False
        objects = models.storage.all()
        print(objects[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
Usage: show <class name> <class id>
Arguments:
    <class name>: Name of the class
    <class id>: Id of the class
"""
        key = serch_clss(arg, True)
        if key is None or not key:
            return False
        objects = models.storage.all()
        del objects[key]
        models.storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances
based or not on the class name.
Usage: show <class name>
Arguments:
    <class name>: Name of the class
Return:
    Print all instances based or not on the class name.
"""
        arg = shlex.split(arg)
        lst = []
        objects = models.storage.all()
        if len(arg) == 0:
            for v in objects.values():
                lst.append(str(v))
            print(lst)
            return False

        if arg[0] in classes:
            for k in objects.keys():
                key = k.split(".")
                if key[0] == arg[0]:
                    lst.append(str(objects[k]))
            print(lst)
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id by
adding or updating attribute
Usage: update <class name> <id> <attribute name> "<attribute value>"
Arguments:
    <class name>: Name of the class
    <class id>: Id of the class
    <attribute name>: Name of the attribute
    <attribute value>: Value of the attribute
    """
        print(arg)
        key = serch_clss(arg, True)
        if key is None or not key:
            return False
        arg = shlex.split(arg)
        if len(arg) == 2:
            print("** attribute name missing **")
            return False
        if len(arg) == 3:
            print("** value missing **")
            return False

        objects = models.storage.all()
        objects[key].__dict__[arg[2]] = arg[3]
        objects[key].save()

        if pid <= 0:
            return True


classes = {"BaseModel": BaseModel, "User": User, "State": State,
           "City": City, "Amenity": Amenity, "Place": Place, "Review": Review}

pid = 1


def serch_clss(arg, ids=False):
    """Search for class or id of an instance
    Parameters:
        arg (string): Arguments
        ids (boolean): Search for id
    Return:
        return False if class doesn't exit or if class missing
        return key if found or None if not found
        return True if class exist
    """
    arg = shlex.split(arg)
    if len(arg) == 0:
        print("** class name missing **")
        return False

    if arg[0] not in classes:
        print("** class doesn't exist **")
        return False

    if ids:
        if len(arg) == 1:
            print("** instance id missing **")
            return False
        objects = models.storage.all()
        for obj in objects.keys():
            key = obj.split(".")
            if key[0] == arg[0] and key[1] == arg[1]:
                return obj
        print("** no instance found **")
        return None
    return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
