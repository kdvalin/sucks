import argparse

from .setup import setup, setup_cli_options
from .destroy import destroy, destroy_cli_options

COMMANDS = {
    "setup": setup,
    "destroy": destroy
}

_SETUP_COMMANDS = [setup_cli_options, destroy_cli_options]

def build_subparsers(subparser: argparse._SubParsersAction):
    for i in _SETUP_COMMANDS:
        i(subparser)

def run_command(command: str, args: argparse.Namespace):
    COMMANDS[command](args)
