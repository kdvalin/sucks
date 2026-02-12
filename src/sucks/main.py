import argparse
import logging
from pydantic import TypeAdapter
import yaml
import os
import pathlib

from . import __version__
from .commands import build_subparsers, run_command
from .models import ContainerDefinition

logger = logging.Logger("sucks")

def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", logging.WARNING).upper())

    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument("container_yaml_file", type=argparse.FileType('r'))
    parser.add_argument("--version", action="version", version=__version__)
    
    subparsers = parser.add_subparsers(help="subcommand help", dest="command")
    build_subparsers(subparsers)
    args = parser.parse_args()

    container_obj = yaml.safe_load(args.container_yaml_file)
    args.container = ContainerDefinition(**container_obj, filename=pathlib.Path(args.container_yaml_file.name).stem)

    run_command(args.command, args)
    
