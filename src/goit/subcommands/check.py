import os

from goit.classes.CheckVHDL import CheckVHDL

_CMD_NAME = os.path.basename(__file__).split('.')[0]
_CMD_HELP = "Perform codebase check"


def command_callback(args):
  if args.extension == "vhd":
    for path in args.paths:
      if path.endswith('.' + args.extension):
        check    = CheckVHDL(path, CheckVHDL.settings)
        elements = check.analyze(check.document, check.settings)
        
        if args.stats:
          print("------------------------------------------------------------------------")
          print("STATS: ", check.file_path)
          print("------------------------------------------------------------------------")
          for line in check.stats(elements, check.settings):
            print(line)
        
        if args.demo:
          print("------------------------------------------------------------------------")
          print("DEMO: ", check.file_path)
          print("------------------------------------------------------------------------")
          for line in check.demo(elements):
            print(line)

        del check


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
  parser = subparsers.add_parser(_CMD_NAME, help=_CMD_HELP)
  parser.add_argument("-i", dest="paths",  required=True,  help="paths of the input files to check", nargs='+', type=lambda file_path: valid_path(parser, file_path))
  parser.add_argument("-e", dest="extension", required=False, help="chooses how to interpret the file", default="vhd", choices=["vhd", "py"])
  parser.add_argument("-d", "--demo",  dest="demo",  required=False, help="prints the pseudo-structure of the file", action='store_true')
  parser.add_argument("-s", "--stats", dest="stats", required=False, help="prints the statistics of found commands and elements", action='store_true')


def valid_path(parser, file_path):
  if not os.path.exists(file_path):
      parser.error("The file %s does not exist!" % file_path)
  else:
      return file_path
