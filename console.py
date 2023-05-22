#!/usr/bin/python3
""" Defines a console for HBnB.
"""
import cmd

import re

import models  # noqa

from shlex import split  # noqa

from models import storage  # noqa

from models.base_model import BaseModel  # noqa

from models.user import User  # noqa

from models.state import State  # noqa

from models.city  import City  # noqa

from models.place import Place  # noqa

from models.amenity import Amenity  # noqa

from models.review import Review  # noqa


def parse(arg):

    curly_braces_match = re.search(r"\{(.*?)\}", arg)

    brackets_match = re.search(r"\[(.*?)\]", arg)

    if curly_braces_match is None:

        if brackets_match is None:

            return [i.strip(",") for i in split(arg)]

        else:

            lexer = split(arg[:brackets_match.span()[0]])

            ret_list = [i.strip(",") for i in lexer]

            ret_list.append(brackets_match.group())

            return ret_list

    else:

        lexer = split(arg[:curly_braces_match.span()[0]])

        ret_list = [i.strip(",") for i in lexer]

        ret_list.append(curly_braces_match.group())

        return ret_list


class HBNBCommand(cmd.Cmd):
    """ This module defines a console"""
    prompt = "(hbnb) "

    __classes = {

        "BaseModel",

        "User",

        "State",

        "City",

        "Place",

        "Amenity",

        "Review"

    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command exits program"""
        return True

    def emptyline(self):
        """ an empty line + ENTER executes nothing"""
        pass

    def do_create(self, arg):

        """Usage: create <class>

        Create a new class instance of BaseModel and print its id.

        """

        arguments = parse(arg)

        if len(arguments) == 0:

            print("** class name missing **")

        elif arguments[0] not in HBNBCommand.__classes:

            print("** class doesn't exist **")

        else:

            print(eval(arguments[0])().id)

            storage.save()

    def do_show(self, arg):
        """
        Prints the str rep of an instance based on the class name and id"""
        arguments = parse(arg)
        object_dict = storage.all()

        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arguments) == 1:
            print("** instance id missing **")
        else:
            instance_key = "{}.{}".format(arguments[0], arguments[1])
            if instance_key not in object_dict:
                print("** no instance found **")
            else:
                print(object_dict[instance_key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        """
        arguments = parse(arg)
        object_dict = storage.all()

        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arguments) == 1:
            print("** instance id missing **")
        else:
            instance_key = "{}.{}".format(arguments[0], arguments[1])
            if instance_key not in object_dict.keys():
                print("** no instance found **")
            else:
                del object_dict[instance_key]
                storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances
            based or not on the class name.
        """
        arguments = parse(arg)
        object_list = []

        if len(arguments) > 0 and arguments[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            for obj in storage.all().values():
                if arguments and arguments[0] == obj.__class__.__name__:
                    object_list.append(str(obj))
                elif len(arguments) == 0:
                    object_list.append(str(obj))
            print(object_list)

    def do_count(self, arg):

        """Retrieve the number of instances of a given class."""

        arguments = parse(arg)

        count = 0

        for obj in storage.all().values():

            if arguments[0] == obj.__class__.__name__:

                count += 1

        print(count)

    def do_update(self, arg):
        """Updates an instance based on the class name and id
            by adding or updating attribute
        """
        arguments = parse(arg)
        object_dict = storage.all()

        if len(arguments) == 0:
            print("** class name missing **")
            return False

        if arguments[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False

        if len(arguments) == 1:
            print("** instance id missing **")
            return False

        instance_key = "{}.{}".format(arguments[0], arguments[1])
        if instance_key not in object_dict.keys():
            print("** no instance found **")
            return False

        if len(arguments) == 2:
            print("** attribute name missing **")
            return False

        if len(arguments) == 3:
            try:
                type(eval(arguments[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arguments) == 4:
            ob = object_dict[instance_key]
            if arguments[2] in ob.__class__.__dict__.keys():
                attribute_type = type(ob.__class__.__dict__[arguments[2]])
                ob.__dict__[arguments[2]] = attribute_type(arguments[3])
            else:
                ob.__dict__[arguments[2]] = arguments[3]
        elif type(eval(arguments[2])) == dict:
            ob = object_dict[instance_key]
            for key, value in eval(arguments[2]).items():
                if (key in ob.__class__.__dict__.keys() and
                        type(ob.__class__.__dict__[key]) in {str, int, float}):
                    attribute_type = type(ob.__class__.__dict__[key])
                    ob.__dict__[key] = attribute_type(value)
                else:
                    ob.__dict__[key] = value

        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
