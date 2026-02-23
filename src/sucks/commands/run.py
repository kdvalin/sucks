import argparse

import podman

from sucks.models import RunArgs

from ._base import Command


class RunCommand(Command):
    _command = "run"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser: argparse.ArgumentParser = subparser.add_parser(self._command)
        RunArgs.add_args(parser)

    def run_command(self, args: RunArgs, client: podman.PodmanClient):
        if not args.conman.exists():
            self._logger.critical(
                f"No container named {args.container.container_name} exists"
            )
            exit(1)

        exit(
            args.conman.exec(
                args.exec_command, args.tty, args.interactive, args.workdir, args.env
            )
        )
