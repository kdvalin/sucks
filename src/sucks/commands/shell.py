import argparse

import podman

from sucks.models import ShellArgs

from ._base import Command


class Shell(Command):
    _command = "shell"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser = subparser.add_parser(self._command)
        ShellArgs.add_args(parser)

    def run_command(self, args: ShellArgs, client: podman.PodmanClient):
        if not args.conman.exists():
            self._logger.critical(
                f"Container {args.container.container_name} does not exist"
            )
            exit(1)
        exit(
            args.conman.exec(
                [args.shell_command], tty=True, interactive=True, workdir=args.workdir
            )
        )
