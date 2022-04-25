#!/usr/bin/env python3
import argparse
from commit_history_file import CommitHistoryFile

def run(args):
    # first_commits = CommitHistoryFile(args.first).read()
    # second_commits = CommitHistoryFile(args.second).read()
    # all_commits = first_commits + second_commits
    # all_commits.sort
    # for commit in all_commits:
    #   print(CommitPrinter(commit).format())
    first_c = CommitHistoryFile().read(args.first)
    second_c = CommitHistoryFile().read(args.second)

    all_c = second_c + first_c

    for commit in all_c[:-1]:
        print(str(commit))
        print()
    print(str(all_c[-1]))


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
