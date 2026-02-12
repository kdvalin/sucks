import argparse
import logging

from . import __version__
from .commands import COMMANDS

def main():
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument("container_yaml_file", type=argparse.FileType('r'))
    parser.add_argument("action", choices=COMMANDS.keys())
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args, unknownargs = parser.parse_known_args()
    COMMANDS[args.action](args.container_yaml_file, unknownargs)
