#!/usr/bin/python3
""" Defines a console for HBnB
"""
import cmd

class HBNBCommand(cmd.Cmd):
    """ This module defines a console"""
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command exits program"""
        return True

    def emptyline(self):
        """ an empty line + ENTER executes nothing"""
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
