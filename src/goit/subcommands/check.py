import argparse
import os

from goit.classes.Check import Check

_CMD_NAME = os.path.basename(__file__).split('.')[0]
_CMD_HELP = "Perform codebase check"


def command_callback(args):
  check = Check(args.filepath)
  check.analyze(check.document)


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
  prser = subparsers.add_parser(_CMD_NAME, help=_CMD_HELP)
  prser.add_argument("-i", dest="filepath", required=True,  help="path of the input file to check", type=lambda file_path: valid_path(prser, file_path))
  prser.add_argument("-v", dest="valid",    required=False, help="validate file if set",            action='store_true')


def valid_path(parser, file_path):
    if not os.path.exists(file_path):
        parser.error("The file %s does not exist!" % file_path)
    else:
        return file_path
