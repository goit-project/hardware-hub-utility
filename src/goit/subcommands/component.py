import argparse
import os

_CMD_NAME = os.path.basename(__file__).split('.')[0]
_CMD_HELP = "Instantiate component into the repository"


def command_callback(args):
  print("Command: " + _CMD_NAME)


def add_command(subcommands, subparsers):
  '''Adds command callback and argument parsing logic to the main utility
     command given dict and subparse objects.

  Parameters
  ----------
    subcommands : dict
      dict object with a key-value form, where key is the name of the command
      and value corresponds to the command callback
        
    subparsers : argparse.subparsers
      subparsers object of the main command parser
  '''

  # add command
  subcommands[_CMD_NAME] = command_callback

  # add subparser and corresponding arguments
  subparsers.add_parser(_CMD_NAME, help=_CMD_HELP)
