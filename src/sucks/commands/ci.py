import argparse
import shlex

from ._base import Command
from sucks.models import BaseArgs

class CICommand(Command):
    _command = "ci"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser = subparser.add_parser(self._command)
    
    def run_command(self, args: BaseArgs, client):
        if not args.conman.exists():
            self._logger.error(f"Container {args.container.container_name} does not exist")
            exit(1)
        
        for step in args.container.ciSteps:
            rtc = args.conman.exec(
                shlex.split(step)
            )

            if rtc != 0:
                self._logger.critical(f"CI step \"{step}\" exited with code {rtc}, exiting")
                exit(rtc)
