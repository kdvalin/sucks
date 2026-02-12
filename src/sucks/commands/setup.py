import logging
import subprocess

import io
from typing import List
from ..models import ContainerDefinition
import argparse

logger = logging.getLogger("sucks")

def setup_cli_options(subparser: argparse._SubParsersAction):
    parser = subparser.add_parser("setup")
    parser.add_argument("-v", "--volume", type=str, action="append", help="A podman volume string to mount a host dir into the container", default=[])
    parser.add_argument("--privileged", action="store_true", help="Give extended priviledges to the container")


def setup(args: argparse.Namespace):
    target_container: ContainerDefinition = args.container
    logger.info(f"Setting up a container from {target_container.image}")
    command = [
        "podman",
        "run",
        "-d", #Detach from the container
        "--name",
        f"sucks-{target_container.filename}"
    ]

    command.extend(f"--volume {vol}" for vol in args.volume)

    if args.privileged:
        command.append('--privileged')
    command.append(target_container.image)

    logger.debug(f"Running \"{" ".join(command)}\"")
    proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if proc.returncode != 0:
        logger.critical(f"Could not initialize {target_container.filename}, see stderr")
        print(proc.stderr.decode('utf-8'))
        exit(1)
    