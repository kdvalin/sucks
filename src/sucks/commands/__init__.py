import argparse

from ._base import Command
from .ci import CICommand
from .destroy import Destroy
from .run import RunCommand
from .setup import Setup
from .shell import Shell

COMMANDS: dict[str, Command] = {}


def setup_commands(subparser: argparse._SubParsersAction):
    _commands_to_setup: list[Command] = [
        Setup(),
        Destroy(),
        RunCommand(),
        Shell(),
        CICommand(),
    ]

    for i in _commands_to_setup:
        COMMANDS[i._command] = i
        i.cli_opts(subparser)
