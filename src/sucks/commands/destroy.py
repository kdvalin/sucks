import logging
import podman

from ._base import Command
from ..models import ContainerDefinition, BaseArgs
import argparse

class Destroy(Command):
    _command = "destroy"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser = subparser.add_parser(self._command)

    def run_command(self, args: BaseArgs, client: podman.PodmanClient):
        self._logger.info(f"Tearing down container named {args.container.container_name}")        

        if not client.containers.exists(args.container.container_name):
            self._logger.error(f"Container {args.container.container_name} does not exist")
            exit(1)
        self._logger.debug(f"Found container {args.container.container_name}")

        client.containers.get(args.container.container_name).kill()
        self._logger.debug("Sent kill command")