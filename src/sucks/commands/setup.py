import io
from typing import List
import argparse

def setup_cli_options(subparser: argparse._SubParsersAction):
    parser = subparser.add_parser("setup")
    parser.add_argument("-v", "--volume", type=str, action="append", help="A podman volume string to mount a host dir into the container")
    parser.add_argument("--privileged", action="store_true", help="Give extended priviledges to the container")


def setup(args: argparse.Namespace):
    print("time for setup")
    print(args.container)