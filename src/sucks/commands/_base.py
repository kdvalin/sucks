import abc
import logging

import argparse
from typing import Dict

class Command(abc.ABC):
    _command = "noop"
    _logger = logging.getLogger("sucks")

    @abc.abstractclassmethod
    def cli_opts(self, subparser: argparse._SubParsersAction) -> None:
        raise NotImplementedError("Function not implemented")

    @abc.abstractclassmethod
    def run_command(self, args: argparse.Namespace) -> None:
        raise NotImplementedError("Function not implemented")

