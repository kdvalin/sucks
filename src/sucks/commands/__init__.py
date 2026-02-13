import argparse
from typing import List, Dict

from ._base import Command, COMMANDS
from .setup import Setup
from .destroy import Destroy

COMMANDS: Dict[str, Command] = {}


def setup_commands(subparser: argparse._SubParsersAction):
    _commands_to_setup: List[Command] = [Setup(), Destroy()]

    for i in _commands_to_setup:
        COMMANDS[i._command] = i
        i.cli_opts(subparser)
