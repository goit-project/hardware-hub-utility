import argparse

def add_command_parser(subparsers):
    subparsers.add_parser("support",   help="Ensure/check support for depending packages and tools")
