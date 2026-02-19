import argparse
import shlex

import podman

from sucks.models import SetupArgs

from ._base import Command


class Setup(Command):
    _command = "setup"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser = subparser.add_parser(self._command)
        SetupArgs.add_args(parser)

    def run_command(self, args: SetupArgs, client: podman.PodmanClient):
        if args.conman.exists():
            self._logger.error(
                f"Container {args.container.container_name} already exists"
            )
            exit(1)

        if not args.conman.pull(args.pull):
            self._logger.critical(f"Could not pull {args.container.image}")
            exit(1)

        create_result = args.conman.create(
            privileged=args.privileged, volumes=args.volume
        )

        if not create_result:
            self._logger.critical(
                f"Could not start container {args.container.container_name}"
            )
            exit(1)

        for step in args.container.initSteps:
            rtc = args.conman.exec(shlex.split(step))

            if rtc != 0:
                self._logger.critical(
                    f'Init step "{step}" exited with code {rtc}, exiting'
                )
                exit(rtc)
