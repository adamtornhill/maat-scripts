import unittest

from capture_stdout_to_list import CaptureStdoutToList
from commit import Commit
from commit_history_report import CommitHistoryReport


class CommitHistoryReportTest(unittest.TestCase):
    def test_given_empty_commit_list_when_print_then_output_is_empty(self):
        # GIVEN empty commit list
        commits = []

        # WHEN printing the commit history
        actual = []
        with CaptureStdoutToList(actual):
            sut = CommitHistoryReport()
            sut.print(commits)

        # THEN output is empty
        self.assertTrue(len(actual) == 0, "print should not produce output")

    def test_given_two_commits_when_print_then_output_is_separated_by_blank_line(self):
        # GIVEN two commits
        commit = self.create_commit()
        commits = [commit, commit]

        # WHEN printing the commit history
        actual = []
        with CaptureStdoutToList(actual):
            sut = CommitHistoryReport()
            sut.print(commits)

        # THEN output is separated by a blank line
        expected = []
        expected.append(commit.first_line)
        expected += commit.change_lines
        expected.append('')
        expected.append(commit.first_line)
        expected += commit.change_lines

        self.assertEqual(expected, actual)

    @staticmethod
    def create_commit():
        result = Commit()
        result.first_line = "[1234567] Some Author 2022-04-25 Some Commit Message"
        result.change_lines = ["1\t2\tsome_file.txt", "3\t4\tanother_file.txt"]
        return result
