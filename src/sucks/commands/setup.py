import logging
import podman

import io
from typing import List
from ..models import ContainerDefinition
import argparse

logger = logging.getLogger("sucks")

def setup_cli_options(subparser: argparse._SubParsersAction):
    parser = subparser.add_parser("setup")
    parser.add_argument("-v", "--volume", type=str, action="append", help="A podman volume string to mount a host dir into the container", default=[])
    parser.add_argument("--privileged", action="store_true", help="Give extended priviledges to the container", default=False)


def setup(args: argparse.Namespace):
    target_container: ContainerDefinition = args.container
    logger.info(f"Setting up a container from {target_container.image}")
    with podman.PodmanClient() as client:
        logging.info(f"Pulling image {target_container.image}")
        try:
            client.images.pull(
                target_container.image
            )
        except podman.errors.APIError as e:
            logger.critical(f"Could not pull container image")
            logger.critical(e)

        try:
            client.containers.create(
                image=target_container.image,
                auto_remove=True,
                detach=True,
                name=f"sucks-{target_container.filename}",
                privileged=args.privileged
            )
        except podman.errors.ImageNotFound as e:
            logger.critical(f"Could find image")
            logger.critical(e)
        except podman.errors.APIError as e:
            logger.critical(f"Could not start container")
            logger.critical(e.explanation)