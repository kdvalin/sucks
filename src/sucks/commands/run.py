import argparse
import subprocess
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

        cmd = ["podman", "exec"]
        if args.tty or args.interactive:
            cmd.append(f"-{"i" if args.interactive else ""}{"t" if args.tty else ""}")
        cmd.append(container_name)
        cmd.extend(args.exec_command)

        proc = subprocess.run(cmd)
        self._logger.info(f"Recevied rtc {proc.returncode}")
        exit(proc.returncode)
