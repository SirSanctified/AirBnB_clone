#!/usr/bin/python3
"""
"""

import cmd
import shlex
from models.base_model import BaseModel


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
        objects = BaseModel.storage.all()
        # print(objects[key])

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
        objects = BaseModel.storage.all()
        # delete instance

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
        objects = BaseModel.storage.all()
        if len(arg) == 0:
            for v in objects.values():
                print(v)
            return False

        if arg[0] in classes:
            for k in objects.keys():
                key = k.split(".")
                if key[0] == arg[0]:
                    print(objects[k])
        else:
            print("** class doesn't exist **")

    # def do_update(self, arg):


classes = {"BaseModel": BaseModel}


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
        objects = BaseModel.storage.all()
        for obj in objects.keys():
            key = obj.split(".")
            if key[0] == arg[0] and key[1] == arg[1]:
                return obj
        print("** no instance found **")
        return None
    return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
