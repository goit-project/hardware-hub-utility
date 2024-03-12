import argparse

def add_command_parser(subparsers):
    subparsers.add_parser("check",     help="Perform codebase check")
