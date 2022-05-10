import unittest

from commit import Commit
from commit_history_report import CommitHistoryReport


class CommitHistoryReportTest(unittest.TestCase):
    def test_given_empty_commit_list_when_print_then_output_is_empty(self):
        commits = []

        sut = CommitHistoryReport()
        actual = sut.generate(commits)

        self.assertTrue(len(actual) == 0, "print should not produce output")

    def test_given_single_commit_when_print_then_output_is_only_the_commit(self):
        commit = self.create_commit()
        commits = [commit]

        sut = CommitHistoryReport()
        actual = sut.generate(commits)

        expected = [commit.first_line] + commit.change_lines
        self.assertEqual('\n'.join(expected), actual)

    def test_given_two_commits_when_print_then_output_is_separated_by_blank_line(self):
        commit = self.create_commit()
        commits = [commit, commit]

        sut = CommitHistoryReport()
        actual = sut.generate(commits)

        expected = [commit.first_line] + commit.change_lines

        expected.append('')

        expected.append(commit.first_line)
        expected += commit.change_lines

        self.assertEqual('\n'.join(expected), actual)

    def test_given_merge_commit_and_ordinary_commit_when_print_then_no_blank_line_between_commits(self):
        merge_commit = Commit()
        merge_commit.first_line = "[1234567] Some Author 2022-04-26 This is a merge commit"
        merge_commit.change_lines = []

        ordinary_commit = self.create_commit()

        commits = [merge_commit, ordinary_commit]

        sut = CommitHistoryReport()
        actual = sut.generate(commits)

        expected = [merge_commit.first_line]

        expected.append(ordinary_commit.first_line)
        expected += ordinary_commit.change_lines

        self.assertEqual('\n'.join(expected), actual)

    @staticmethod
    def create_commit():
        result = Commit()
        result.first_line = "[1234567] Some Author 2022-04-25 Some Commit Message"
        result.change_lines = ["1\t2\tsome_file.txt", "3\t4\tanother_file.txt"]
        return result
