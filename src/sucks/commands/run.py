import argparse
import podman
import logging

from ._base import Command
from sucks.models import ContainerDefinition

class RunCommand(Command):
    _command = "run"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser: argparse.ArgumentParser = subparser.add_parser(self._command)

        parser.add_argument("-w", "--workdir", help="Set working dir the command is run in")
        parser.add_argument("-e", "--env", help="Set enviornment variables", action="append", default=[])
        parser.add_argument("-i", "--interactive", help="Pass stdin to the command", action="store_true", default=False)
        parser.add_argument("-t", "--tty", help="Allocate a pseudo-TTY", action="store_true", default=False)
        parser.add_argument("exec_command", nargs="+", help="The command to run within the container")

    def run_command(self, args: argparse.Namespace, client: podman.PodmanClient):
        container_def: ContainerDefinition = args.container
        container_name = f"sucks-{container_def.filename}"

        if not client.containers.exists(container_name):
            self._logger.critical(f"No container named {container_name} exists")
            exit(1)
        
        self._logger.info(f"Running \"{" ".join(args.exec_command)}\" in {container_name}")
        rtc, output = client.containers.get(container_name).exec_run(
            args.exec_command
        )

        print(output.decode('utf-8'), end="")
        self._logger.info(f"Got return code {rtc}")
        exit(rtc)
