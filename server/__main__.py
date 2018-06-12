#! /usr/bin/python

"""
[SERVER] Unsupervised Parkinson's Disease Assessment

Date:       Tuesday June 12th, 2018
Author:     Alexander Adranly

Console class
"""
from server import *


"""
[CLASS] Command

Defines a new command a user can install into the console class
"""


class Command(object):

    def __init__(self, name, help_msg, action):
        self.__name = name
        self.__help = help_msg
        self.__action = action

    def name(self):
        """
        :return: (str) name of the command
        """
        return self.__name

    def __call__(self, tokens):
        """
        :param tokens: (list) : arguments from user input that can be used to run the command
        :return:
        """
        self.__action(tokens)

    def __str__(self):
        """
        :return: (str) : string formatted description of what is shown in the "help" menu
        """
        return self.__name + ('\t' * 3) + self.__help


"""
[CLASS] Console

Defines a generic class for designing a basic console interface for the application.
New command objects can be created and added to the console class to enable different
types of features.
"""


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

    def set_prompt(self, prompt):
        """
        :param prompt: (str) : prompt to set
        :return: NA
        """
        self.__prompt = prompt

    def set_separator(self, sep):
        """
        :param sep: (str): seperator  to set
        :return: NA
        """
        self.__separator = sep

    def set_closer(self, close):
        """
        :param close: (str): set an exit message
        :return: NA
        """

        self.__closer = close

    def add_command(self, command):
        """
        :param command: (Command) : command to be added to console
        :return: NA
        """
        if not type(command) is Command:
            print("invalid command to add")
            return

        if not command.name() in self.__commands:
            self.__commands[command.name()] = command

    def cmd_help(self, tokens):
        """
        Function for the help command
        :param tokens: (list): arguments to pass to the command
        :return:  NA
        """

        print("usage: {}\n".format(self.__name))
        for cmd in self.__commands.items():
            print(cmd[1])

    def cmd_exit(self, tokens):
        """
        Signal the thread to terminate the console
        Called upon the "exit" command
        :param tokens: arguments
        :return:
        """
        self.__run = False

    def run(self):
        """
        Main loop that drives the console
        :return:
        """
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
    """
    The function that defines the console and starts the entire
    software system on the server
    :return:
    """
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
    test_cmd = Command(name='test', help_msg='command to easily test new code features', action=test_module)

    # add commands
    console.add_command(start_cmd)
    console.add_command(stats_cmd)
    console.add_command(load_cmd)
    console.add_command(list_cmd)
    console.add_command(test_cmd)

    # console.run()
    console.run()


if __name__ == '__main__':
    main()
