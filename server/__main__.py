#! /usr/bin/python

"""
run_server.py

by Alexander Adranly, 2018


Building the tools for an effective command line interface
"""
from server import *


class Command(object):

    def __init__(self, name, help_msg, action):
        self.__name = name
        self.__help = help_msg
        self.__action = action

    def name(self):
        return self.__name

    def __call__(self, tokens):
        self.__action(tokens)

    def __str__(self):
        return self.__name + ('\t' * 3) + self.__help


class Console(object):

    def __init__(self, name):
        self.__name = name
        self.__prompt = "> "
        self.__separator = ' '
        self.__closer = "goodbye"
        # list of command objects
        self.__commands = dict()
        self.__commands['help'] = Command(name="help", help_msg="description of how to use the commands", action=self.cmd_help)
        self.__commands['exit'] = Command(name='exit', help_msg='exits the console', action=self.cmd_exit)
        # control objects
        self.__run = True

    """
        SETTERS
    """

    def set_prompt(self, prompt):
        self.__prompt = prompt

    def set_separator(self, sep):
        self.__separator = sep

    def set_closer(self, close):
        self.__closer = close

    """
        COMMANDS
    """

    def add_command(self, command):
        if not type(command) is Command:
            print("invalid command to add")
            return

        if not command.name() in self.__commands:
            self.__commands[command.name()] = command

    def cmd_help(self, tokens):
        print("usage: {}\n".format(self.__name))
        for cmd in self.__commands.items():
            print(cmd[1])

    def cmd_exit(self, tokens):
        self.__run = False

    """
        RUNNING SYSTEM
    """

    def run(self):
        try:
            while self.__run:
                tokens = input(self.__prompt).lower().split(sep=self.__separator)
                # print(tokens)
                if tokens[0] in self.__commands:
                    # running command
                    self.__commands[tokens[0]](tokens)

                else:
                    print("unknown cmd '{}'".format(tokens[0]))

                print()

        except KeyboardInterrupt:
            pass

        finally:
            print(self.__closer)


def main():

    print('*' * 50)
    print("\n  .----.-----.-----.-----.\n",
          "/      \     \     \     \\\n",
          "|  \/    |     |   __L_____L__\n",
          "|   |    |     |  (           \\\n",
          "|    \___/    /    \______/    |\n",
          "|        \___/\___/\___/       |\n",
          "|      \     /               /\n",
          "|                        __/\n",
          "\_                   __/\n",
          "|        |         |\n",
          "|                  |\n",
          "|                  |\n\n")

    print("UPDA Console")
    print("Version {}".format(VERSION), '\n')
    print('*' * 50, '\n')

    console = Console("UPDA Console")

    # generate all commands
    start_cmd = Command(name='start', help_msg='start a subroutine (start server|process)', action=start)
    stats_cmd = Command(name='stat', help_msg='produce statistics about the previous server runtime', action=stats)
    load_cmd = Command(name='load', help_msg='load data from the sd card and write to the server', action=load)
    list_cmd = Command(name='list', help_msg='list specified items. ex: list patients', action=list_items)

    # add commands
    console.add_command(start_cmd)
    console.add_command(stats_cmd)
    console.add_command(load_cmd)
    console.add_command(list_cmd)

    # console.run()
    console.run()


if __name__ == '__main__':
    main()
