#!/usr/bin/env python3
import argparse
from commit_history_file import CommitHistoryFile
from commit_formatter import CommitFormatter

def run(args):
    # first_commits = CommitHistoryFile(args.first).read()
    # second_commits = CommitHistoryFile(args.second).read()
    # all_commits = first_commits + second_commits
    # all_commits.sort
    # for commit in all_commits:
    #   print(CommitPrinter(commit).format())

    first_commits = CommitHistoryFile().read(args.first)
    second_commits = CommitHistoryFile().read(args.second)

    second_commits.append('')
    all_commits = second_commits + first_commits

    formatter = CommitFormatter()
    for commit in all_commits:
        print(formatter.format(commit))


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
