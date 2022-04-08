#!/usr/bin/env python3
import argparse


def run(args):
    first = read_file(args.first)
    second = read_file(args.second)

    second.append('')
    combined = second + first

    for line in combined:
        print(line)


def read_file(path):
    with open(path, 'rt') as f:
        contents = f.read().splitlines()
    return contents


def create_argument_parser():
    desc = "Combines two git history files into one."
    parser = argparse.ArgumentParser(
        description=desc)
    parser.add_argument('first', help="first git history file")
    parser.add_argument('second', help="second git history file")
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()

    args = parser.parse_args()
    run(args)
