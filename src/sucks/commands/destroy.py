import logging
import podman

from ._base import Command
from ..models import ContainerDefinition
import argparse

logger = logging.getLogger("sucks")


class Destroy(Command):
    _command = "destroy"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser = subparser.add_parser(self._command)


    def run_command(self, args: argparse.Namespace, client: podman.PodmanClient):
        target_container: ContainerDefinition = args.container
        container_name = f"sucks-{target_container.filename}"
        logger.info(f"Tearing down container named {container_name}")        

        if not client.containers.exists(container_name):
            logger.error(f"Container sucks-{target_container.filename} does not exist")
            exit(1)
        logger.debug(f"Found container {container_name}")        

        client.containers.get(container_name).kill()
        logger.debug("Sent kill command")