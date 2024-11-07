import argparse
import os

from goit.classes.ComponentVHDL import ComponentVHDL
from goit.classes.dependencies.DependencySolverHDLMake import DependencySolverHDLMake

_CMD_NAME = os.path.basename(__file__).split('.')[0]
_CMD_HELP = "Temporary command for testing utilities' codebase features"


def command_callback(args):
  solver = DependencySolverHDLMake()
  solver.populate_dependencies(args.wildcard)
  deps_list = solver.get_dependencies()

  for d in deps_list:
    print(d)


def add_command(subcommands, subparsers):
  '''Temporary command for testing utilities' codebase features'''

  # add command
  subcommands[_CMD_NAME] = command_callback

  # add subparser and corresponding arguments
  parser = subparsers.add_parser(_CMD_NAME, help=_CMD_HELP)
  parser.add_argument("-d", "--dependency", action="store_true",  help="Provide dependencies")
  parser.add_argument("wildcard",                                 help="Path to the component(s)")
