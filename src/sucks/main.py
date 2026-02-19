import argparse
import logging
import os
import pathlib

import podman
import yaml

import sucks.commands

from . import __version__
from .models import BaseArgs, ContainerDefinition
from .utils import ContainerManager

logger = logging.getLogger("sucks")


def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING").upper())

    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument("container_yaml_file", type=argparse.FileType("r"))
    parser.add_argument("--version", action="version", version=__version__)

    subparsers = parser.add_subparsers(
        help="subcommand help", dest="command", required=True
    )
    sucks.commands.setup_commands(subparsers)
    args: BaseArgs = parser.parse_args()

    container_obj = yaml.safe_load(args.container_yaml_file)
    args.container = ContainerDefinition(
        **container_obj, filename=pathlib.Path(args.container_yaml_file.name).stem
    )

    if args.workdir is None and args.container.workdir is not None:
        args.workdir = args.container.workdir

    with podman.PodmanClient() as client:
        if not client.ping():
            logging.critical("Cannot communicate with podman socket")
            exit(1)
        args.conman = ContainerManager(args.container, client)
        sucks.commands.COMMANDS[args.command].run_command(args, client)
