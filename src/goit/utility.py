#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK
import argparse
import argcomplete


parser = argparse.ArgumentParser()

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

argcomplete.autocomplete(parser)
args = parser.parse_args()
