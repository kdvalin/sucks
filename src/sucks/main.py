import argparse
import logging

from . import __version__

def main():
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument("container_yaml_file", type=argparse.FileType('r'))
    parser.add_argument("action", type=str) #TODO make this a dynamic import to the other bits
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args, unknownargs = parser.parse_known_args()
    print(args)
    print(unknownargs)