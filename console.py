#!/usr/bin/python3
"""
"""

import cmd
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import models


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def emptyline(self):
        """Overide the emptyline method to skip emptyl line"""
        return False

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


classes = {"BaseModel": BaseModel, "User": User, "State": State,
           "City": City, "Amenity": Amenity, "Place": Place, "Review": Review}


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
