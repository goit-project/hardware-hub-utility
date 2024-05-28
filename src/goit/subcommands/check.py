import os

from goit.classes.CheckVHDL import CheckVHDL

_CMD_NAME = os.path.basename(__file__).split('.')[0]
_CMD_HELP = "Perform codebase check"


def command_callback(args):
  if args.extension == "vhdl": 
    check = CheckVHDL(args.filepath)
    check.analyze(check.document)
    
    if args.stats:
      check.print_stats()
    
    if args.demo:
      check.print_demo(args)


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
  prser.add_argument("-i", dest="filepath",  required=True,  help="path of the input file to check", type=lambda file_path: valid_path(prser, file_path))
  prser.add_argument("-e", dest="extension", required=False, help="chooses how to interpret the file", default="vhdl", choices=["vhdl", "py"])
  prser.add_argument("-d", "--demo",  dest="demo",  required=False, help="prints the pseudo-structure of the file", action='store_true')
  prser.add_argument("-s", "--stats", dest="stats", required=False, help="prints the statistics of found commands and elements", action='store_true')


def valid_path(parser, file_path):
    if not os.path.exists(file_path):
        parser.error("The file %s does not exist!" % file_path)
    else:
        return file_path
