import argparse
import podman
import logging

from ._base import Command
from sucks.models import ContainerDefinition, SetupArgs

from typing import List, Dict

class Setup(Command):
    _command = "setup"

    def _parse_volume_strs(self, vols: List[str]) -> Dict[str, object]:
        output = {}

        for vol in vols:
            vol_args = vol.split(':')

            if len(vol_args) < 2 or len(vol_args) > 3:
                self._logger.warning(f"Volume string {vol} does not match expected format, skipping")
                continue
            
            host_dir = vol_args[0]
            container_dir = vol_args[1]
            extended_opts = []
            if len(vol_args) == 3:
                extended_opts = vol_args[2].split(',')

            output[host_dir] = {
                'bind': container_dir,
                'extended_mode': extended_opts,
            }
        return output            

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser = subparser.add_parser(self._command)
        SetupArgs.add_args(parser)


    def run_command(self, args: SetupArgs, client: podman.PodmanClient):
        container_def: ContainerDefinition = args.container
        container_name = f"sucks-{container_def.filename}"
        
        if client.containers.exists(container_name):
            self._logger.error(f"Container {container_name} already exists")
            exit(1)
        
        try:
            client.images.pull(container_def.image)
        except podman.errors.APIError as e:
            self._logger.critical(f"Could not pull {container_def.image}")
            self._logger.critical(e)
            exit(1)
        
        try:
            client.containers.create(
                container_def.image,
                name=container_name,
                auto_remove=True,
                privileged=args.privileged,
                volumes=self._parse_volume_strs(args.volume)
            ).start()
        except podman.errors.APIError as e:
            self._logger.critical(f"Could not start contianer")
            self._logger.critical(e)
            exit(1)
