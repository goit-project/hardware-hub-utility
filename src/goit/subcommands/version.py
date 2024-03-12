import argparse

def add_command_parser(subparsers):
    subparsers.add_parser("version",   help="Get version local/upstream versions")
