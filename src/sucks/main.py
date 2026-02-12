import argparse
import logging
from pydantic import TypeAdapter
import yaml

from . import __version__
from .commands import build_subparsers, run_command
from .models import ContainerDefinition

def main():
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument("container_yaml_file", type=argparse.FileType('r'))
    parser.add_argument("--version", action="version", version=__version__)
    
    subparsers = parser.add_subparsers(help="subcommand help", dest="command")
    build_subparsers(subparsers)
    args = parser.parse_args()

    container_obj = yaml.safe_load(args.container_yaml_file)
    container_def = ContainerDefinition(**container_obj)
    
    args.container = container_def

    run_command(args.command, args)
    
