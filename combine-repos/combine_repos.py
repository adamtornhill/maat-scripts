#!/usr/bin/env python3
import argparse
from contextlib import redirect_stdout

from commit_history_reader import CommitHistoryReader
from commit_history_report import CommitHistoryReport


# TODO: Add -outfile parameter to specify the result file
# TODO: Add documentation
def run(args):
    first_commits = CommitHistoryReader().read(args.first)
    second_commits = CommitHistoryReader().read(args.second)

    all_commits = second_commits + first_commits

    all_commits.sort(key=lambda commit: commit.date, reverse=True)

    if args.output is not None:
        with open(args.output, 'w') as f:
            with redirect_stdout(f):
                CommitHistoryReport().print(all_commits)
    else:
        CommitHistoryReport().print(all_commits)


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
