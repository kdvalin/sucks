import logging
import podman

from ._base import Command
from ..models import ContainerDefinition
import argparse

class Destroy(Command):
    _command = "destroy"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser = subparser.add_parser(self._command)


    def run_command(self, args: argparse.Namespace, client: podman.PodmanClient):
        target_container: ContainerDefinition = args.container
        container_name = f"sucks-{target_container.filename}"
        self._logger.info(f"Tearing down container named {container_name}")        

        if not client.containers.exists(container_name):
            self._logger.error(f"Container sucks-{target_container.filename} does not exist")
            exit(1)
        self._logger.debug(f"Found container {container_name}")        

        client.containers.get(container_name).kill()
        self._logger.debug("Sent kill command")