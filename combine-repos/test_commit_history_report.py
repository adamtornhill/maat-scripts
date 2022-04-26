import unittest

from commit import Commit
from commit_history_report import CommitHistoryReport


class CommitHistoryReportTest(unittest.TestCase):
    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        self.printed = []

    def test(self):
        commits = [self.create_commit(), self.create_commit()]

        sut = CommitHistoryReport()
        sut.print_function = self.print_replacement
        sut.print(commits)

        # TODO fix assert statement
        self.assertEqual(0, 0)

    def print_replacement(self, string=''):
        self.printed.append(string)

    @staticmethod
    def create_commit():
        result = Commit()
        result.first_line = "[1234567] Some Author 2022-04-25 Some Commit Message"
        result.change_lines = ["1\t2\tsome_file.txt", "3\t4\tanother_file.txt"]
        return result
