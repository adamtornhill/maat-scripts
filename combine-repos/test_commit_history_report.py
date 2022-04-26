import contextlib
import io
import unittest

from commit import Commit
from commit_history_report import CommitHistoryReport


class CommitHistoryReportTest(unittest.TestCase):
    def test_given_two_commits_when_print_then_returned_output_is_separated_by_blank_line(self):
        # GIVEN two commits
        commit = self.create_commit()
        commits = [commit, commit]

        # WHEN printing the commit history
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            sut = CommitHistoryReport()
            sut.print(commits)
        actual = buffer.getvalue().split('\n')

        # split inserts a blank line at the end, if the last line in the buffer ends with '\n'
        # remove this wrong indicator of a blank line where there is none
        actual = actual[:-1]

        # THEN returned output is separated by a blank line
        expected = []
        expected.append(commit.first_line)
        expected += commit.change_lines
        expected.append('')
        expected.append(commit.first_line)
        expected += commit.change_lines

        self.assertEqual(actual, expected)

    @staticmethod
    def create_commit():
        result = Commit()
        result.first_line = "[1234567] Some Author 2022-04-25 Some Commit Message"
        result.change_lines = ["1\t2\tsome_file.txt", "3\t4\tanother_file.txt"]
        return result
