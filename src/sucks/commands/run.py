import argparse
import subprocess
import logging

from ._base import Command
from sucks.models import ContainerDefinition, RunArgs

class RunCommand(Command):
    _command = "run"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser: argparse.ArgumentParser = subparser.add_parser(self._command)
        RunArgs.add_args(parser)

    def run_command(self, args: RunArgs, client: podman.PodmanClient):
        container_def: ContainerDefinition = args.container
        container_name = f"sucks-{container_def.filename}"

        if not client.containers.exists(container_name):
            self._logger.critical(f"No container named {container_name} exists")
            exit(1)
        
        self._logger.info(f"Running \"{" ".join(args.exec_command)}\" in {container_name}")

        cmd = ["podman", "exec"]
        if args.tty or args.interactive:
            cmd.append(f"-{"i" if args.interactive else ""}{"t" if args.tty else ""}")
        
        if args.workdir != None:
            cmd.extend(["-w", args.workdir])
        cmd.append(container_name)
        cmd.extend(args.exec_command)

        proc = subprocess.run(cmd)
        self._logger.info(f"Recevied rtc {proc.returncode}")
        exit(proc.returncode)
