import argparse

from sucks.utils import ContainerManager

from .container_file import ContainerDefinition


class BaseArgs(argparse.Namespace):
    container_yaml_file: str
    container: ContainerDefinition
    conman: ContainerManager
    workdir: str

    @staticmethod
    def add_args(parser: argparse.ArgumentParser):
        parser.add_argument(
            "-w",
            "--workdir",
            type=str,
            help="Sets the workdir that the setup, ci, run, and shell commands run in",
            default=None,
        )


class SetupArgs(BaseArgs):
    volume: list[str]
    privileged: bool
    pull: str

    @staticmethod
    def add_args(parser: argparse.ArgumentParser):
        parser.add_argument(
            "-v",
            "--volume",
            type=str,
            action="append",
            help="A podman volume string to mount a host dir into the container",
            default=[],
        )
        parser.add_argument(
            "--pull",
            choices=["always", "missing", "never", "newer"],
            help="Sets when to pull an image",
            default="missing",
        )
        parser.add_argument(
            "--privileged",
            action="store_true",
            help="Give extended privileges to the container",
            default=False,
        )
        BaseArgs.add_args(parser)


class RunArgs(BaseArgs):
    workdir: str
    env: list[str]
    interactive: bool
    tty: bool
    exec_command: list[str]

    @staticmethod
    def add_args(parser: argparse.ArgumentParser):
        parser.add_argument(
            "-e", "--env", help="Set environment variables", action="append", default=[]
        )
        parser.add_argument(
            "-i",
            "--interactive",
            help="Pass stdin to the command",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "-t",
            "--tty",
            help="Allocate a pseudo-TTY",
            action="store_true",
            default=False,
        )
        BaseArgs.add_args(parser)
        parser.add_argument(
            "exec_command", nargs="+", help="The command to run within the container"
        )


class ShellArgs(BaseArgs):
    shell_command: str

    @staticmethod
    def add_args(parser: argparse.ArgumentParser):
        BaseArgs.add_args(parser)
        parser.add_argument(
            "-s",
            "--shell_command",
            help="The command to run for the shell",
            default="bash",
            type=str,
        )
