import unittest

from commit import Commit


class CommitStrTest(unittest.TestCase):
    def test_given_commit_and_change_line_when_str_then_return_two_lined_string(self):
        commit = Commit()
        commit.first_line = '[1234567] Some Author 2022-05-09 Some comment'
        commit.change_lines = ['1\t2\tsome_file.txt']

        actual = str(commit)

        expected = '[1234567] Some Author 2022-05-09 Some comment\n' \
                   '1\t2\tsome_file.txt'
        self.assertEqual(expected, actual)

    def test_given_commit_without_change_line_when_str_then_return_single_line_string(self):
        commit = Commit()
        commit.first_line = '[1234567] Some Author 2022-05-09 Some comment'
        commit.change_lines = []

        actual = str(commit)

        expected = '[1234567] Some Author 2022-05-09 Some comment'
        self.assertEqual(expected, actual)
