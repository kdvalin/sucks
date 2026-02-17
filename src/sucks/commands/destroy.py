import argparse
import podman

from ._base import Command
from ..models import BaseArgs

class Destroy(Command):
    _command = "destroy"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser = subparser.add_parser(self._command)

    def run_command(self, args: BaseArgs, client: podman.PodmanClient):
        self._logger.info(f"Tearing down container named {args.container.container_name}")        

        if not args.conman.exists():
            self._logger.error(f"Container {args.container.container_name} does not exist")
            exit(1)
        self._logger.debug(f"Found container {args.container.container_name}")

        args.conman.kill()
        self._logger.debug("Sent kill command")