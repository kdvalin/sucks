import logging
import podman
from ..utils import container_exists

import io
from typing import List
from ..models import ContainerDefinition
import argparse

logger = logging.getLogger("sucks")

def destroy_cli_options(subparser: argparse._SubParsersAction):
    parser = subparser.add_parser("destroy")


def destroy(args: argparse.Namespace):
    target_container: ContainerDefinition = args.container
    container_name = f"sucks-{target_container.filename}"
    logger.info(f"Tearing down container named {container_name}")
    

    with podman.PodmanClient() as client:
        if not client.containers.exists(container_name):
            logger.error(f"Container sucks-{target_container.filename} does not exist")
            exit(1)
        logger.debug(f"Found container {container_name}")        

        client.containers.get(container_name).kill()
        logger.debug("Sent kill command")