#!/usr/bin/env python3
import argparse
from pipe import *

from commit_history_reader import CommitHistoryReader
from commit_history_report import CommitHistoryReport


def print_report(outfile, report):
    if report == '':
        return

    if outfile is not None:
        with open(outfile, 'w') as f:
            f.write(report)
    else:
        print(report)


def run(args):
    input_files = [args.first, args.second] + args.other

    all_commits = list(input_files
                       | map(lambda file: CommitHistoryReader().read(file))
                       | traverse
                       | sort(key=lambda commit: commit.date, reverse=True))

    report = CommitHistoryReport().generate(all_commits)
    print_report(args.output, report)


def create_argument_parser():
    desc = """Combine a number of git history files into a single git history file.
              The program sorts the aggregated commits by date in descending order before writing the result."""
    result = argparse.ArgumentParser(description=desc)
    result.add_argument('first', help="first git history file")
    result.add_argument('second', help="second git history file")
    result.add_argument('other', nargs='*', help="optional list of additional git history files")
    result.add_argument('--output', type=str, help="path to a file which shall receive the result")
    return result


if __name__ == "__main__":
    parser = create_argument_parser()

    args = parser.parse_args()
    run(args)
