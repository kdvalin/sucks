import argparse
import logging

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("container_yaml_file", type=argparse.FileType('r'))
    parser.add_argument("action", type=str) #TODO make this a dynamic import to the other bits
    args, unknownargs = parser.parse_known_args()
    print(args)
    print(unknownargs)