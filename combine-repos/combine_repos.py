#!/usr/bin/env python3
import argparse

from commit_history_reader import CommitHistoryReader
from commit_history_report import CommitHistoryReport


# TODO: Add documentation
def run(args):
    first_commits = CommitHistoryReader().read(args.first)
    second_commits = CommitHistoryReader().read(args.second)

    all_commits = second_commits + first_commits

    all_commits.sort(key=lambda commit: commit.date, reverse=True)

    report = CommitHistoryReport().generate(all_commits)
    print_report(args.output, report)


def print_report(outfile, report):
    if report != '':
        if outfile is not None:
            with open(outfile, 'w') as f:
                f.write(report)
        else:
            print(report)


def create_argument_parser():
    desc = "Combines two git history files into one."
    parser = argparse.ArgumentParser(
        description=desc)
    parser.add_argument('first', help="first git history file")
    parser.add_argument('second', help="second git history file")
    parser.add_argument('--output', type=str, help="path to a file which shall receive the result")
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()

    args = parser.parse_args()
    run(args)
