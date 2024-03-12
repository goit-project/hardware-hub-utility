import argparse

def add_command_parser(subparsers):
    subparsers.add_parser("package",   help="Instantiate package (routine) file into the repository")
