#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK
import sys
import argparse
import argcomplete
# TODO automate
sys.path.append("..")
import goit.subcommands.support
import goit.subcommands.check
import goit.subcommands.component
import goit.subcommands.package
import goit.subcommands.version
import goit.subcommands.help


# TODO (functionality): instantiate component / library
# - argument, set create (component, package)
# - argument, set library (selection, default)
# - argument, set language (selection)
# - argument, set name (mandatory)
#
# TODO (functionality): simulation
# - argument, test scope (all, library, component, default)
# - argument, test scope (simulation tool, auto)
#
# TODO (functionality): check documentation
#
# TODO (functionality): compare tool version with upstream
#
# TODO (functionality): check interface compatibility
#
# TODO (functionality): check naming conventions
#
# TODO (functionality): check tool availability in the environment
# - simulation (at least one)
#   - ghdl
#   - verilator
#   - icarus
# - dependency solver (at least one)
#   - hdlmake
#   - FuseSoC
#   - others
# - others
#   - yosys (for test coverage)
#
# TODO (functionality): generate target project / update dependencies?


def main():
  # setup argument parser without default --help option
  parser = argparse.ArgumentParser()
  parser = argparse.ArgumentParser(add_help=False)

  # create placeholder for commands
  subcommands = {}

  # define tool's mutually exclusive commands
  subparsers = parser.add_subparsers(dest="cmd")

  # create mutually exclusive commands/parsers (TODO: automate)
  goit.subcommands.check.add_command(subcommands, subparsers)
  goit.subcommands.component.add_command(subcommands, subparsers)
  goit.subcommands.package.add_command(subcommands, subparsers)
  goit.subcommands.support.add_command(subcommands, subparsers)
  goit.subcommands.version.add_command(subcommands, subparsers)
  goit.subcommands.help.add_command(subcommands, subparsers)

  # this produces autocomplete (if properly enabled)
  argcomplete.autocomplete(parser)

  # parse the arguments
  args = parser.parse_args()

  # generic way to invoke subcommands, with the somewhat sad workaround
  # for help, where we use parser object to generate the message
  if args.cmd == 'help':
    subcommands[args.cmd](parser)
  elif args.cmd in subcommands:
    subcommands[args.cmd](args)
  else:
    print("Invoked erroneous command: %s" %(args.cmd))


if __name__ == "__main__":
    main()
