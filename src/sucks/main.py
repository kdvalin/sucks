import argparse
import logging

from . import __version__
from .commands import build_subparsers, run_command

def main():
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument("container_yaml_file", type=argparse.FileType('r'))
    parser.add_argument("--version", action="version", version=__version__)
    
    subparsers = parser.add_subparsers(help="subcommand help", dest="command")
    build_subparsers(subparsers)
    args = parser.parse_args()

    run_command(args.command, args)
    
