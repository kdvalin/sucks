import argparse
import podman
import logging

from ._base import Command
from sucks.models import ContainerDefinition

logger = logging.Logger("sucks")

class Setup(Command):
    _command = "setup"

    def cli_opts(self, subparser: argparse._SubParsersAction):
        parser = subparser.add_parser(self._command)
        parser.add_argument("-v", "--volume", type=str, action="append", help="A podman volume string to mount a host dir into the container", default=[])
        parser.add_argument("--privileged", action="store_true", help="Give extended priviledges to the container", default=False)


    def run_command(self, args: argparse.Namespace, client: podman.PodmanClient):
        container_def: ContainerDefinition = args.container
        container_name = f"sucks-{container_def.filename}"
        
        if client.containers.exists(container_name):
            logger.error(f"Container {container_name} already exists")
            exit(1)
        
        try:
            client.images.pull(container_def.image)
        except podman.errors.APIError as e:
            logger.critical(f"Could not pull {container_def.image}")
            logger.critical(e)
            exit(1)
        
        try:
            client.containers.create(
                container_def.image,
                name=container_name
            ).start()
        except podman.errors.APIError as e:
            logger.critical(f"Could not start contianer")
            logger.critical(e)
            exit(1)
