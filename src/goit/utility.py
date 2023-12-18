#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK
import argparse
import argcomplete


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
    parser = argparse.ArgumentParser()

    # define tool's mutually exclusive commands
    subparsers = parser.add_subparsers(dest="cmd")

    # create mutually exclusive commands/parsers
    subparsers.add_parser("support",   help="Ensure/check support for depending packages and tools")
    subparsers.add_parser("component", help="Instantiate component into the repository")
    subparsers.add_parser("package",   help="Instantiate package (routine) file into the repository")
    subparsers.add_parser("version",   help="Get version local/upstream versions")
    subparsers.add_parser("check",     help="Perform codebase check")

    # this produces autocomplete (if properly enabled)
    argcomplete.autocomplete(parser)

    # parse the arguments
    args = parser.parse_args()

    print("Invoked command: %s" %(args.cmd))


if __name__ == "__main__":
    main()
