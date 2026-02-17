import argparse
from typing import List

from .container_file import ContainerDefinition
from sucks.utils import ContainerManager

class BaseArgs(argparse.Namespace):
    container_yaml_file: str
    container: ContainerDefinition
    conman: ContainerManager

class SetupArgs(BaseArgs):
    volume: List[str]
    privileged: bool

    def add_args(parser: argparse.ArgumentParser):
        parser.add_argument("-v", "--volume", type=str, action="append", help="A podman volume string to mount a host dir into the container", default=[])
        parser.add_argument("--privileged", action="store_true", help="Give extended privileges to the container", default=False)


class RunArgs(BaseArgs):
    workdir: str
    env: List[str]
    interactive: bool
    tty: bool
    exec_command: List[str]

    def add_args(parser: argparse.ArgumentParser):
        parser.add_argument("-w", "--workdir", help="Set working dir the command is run in")
        parser.add_argument("-e", "--env", help="Set environment variables", action="append", default=[])
        parser.add_argument("-i", "--interactive", help="Pass stdin to the command", action="store_true", default=False)
        parser.add_argument("-t", "--tty", help="Allocate a pseudo-TTY", action="store_true", default=False)
        parser.add_argument("exec_command", nargs="+", help="The command to run within the container")

class ShellArgs(BaseArgs):
    shell_command: str

    def add_args(parser: argparse.ArgumentParser):
        parser.add_argument("-s", "--shell_command", help="The command to run for the shell", default="bash", type=str)
