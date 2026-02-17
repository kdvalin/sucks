import argparse
import podman
from ._base import Command
from .run import RunCommand
from sucks.models import ShellArgs, RunArgs

class Shell(Command):
    _command = "shell"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser = subparser.add_parser(self._command)
        ShellArgs.add_args(parser)

    def run_command(self, args: ShellArgs, client: podman.PodmanClient):
        new_args: RunArgs = args
        new_args.interactive = True
        new_args.tty = True
        new_args.exec_command = [args.shell_command]
        new_args.workdir = "/root"
        RunCommand().run_command(new_args, client)