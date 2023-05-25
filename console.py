#!/usr/bin/python3
""" Defines a console for HBnB.
"""
import cmd
import re
import models  # noqa
from shlex import split
from models import storage
from models.base_model import BaseModel  # noqa
from models.user import User  # noqa
from models.state import State  # noqa
from models.city import City  # noqa
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

    def default(self, arg):
        """Handle invalid commands.
        Args:
            arg (str): The input command.
        Returns:
            bool: False indicating the command was not valid.
        """
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance of BaseModel and print its id.
        """
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """
        Prints the str rep of an instance based on the class name and id"""
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        """
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances
            based or not on the class name.
        """
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Retrieve the number of instances of a given class."""
        argument = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argument[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Updates an instance based on the class name and id
            by adding or updating attribute
        """
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()



if __name__ == '__main__':
    HBNBCommand().cmdloop()
