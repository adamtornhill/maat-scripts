import contextlib
import io
import unittest

import combine_repos


class CombineReposTest(unittest.TestCase):
    def test_concatenate_git_history_files(self):
        # SCENARIO Simply concatenate git history files
        parser = combine_repos.create_argument_parser()

        # GIVEN I have two git history files
        args = ["test-data/concatenate/first_evo.log", "test-data/concatenate/second_evo.log"]

        # WHEN I combine the git history files
        args = parser.parse_args(args)
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            combine_repos.run(args)

        # THEN the combined history is printed to stdout
        with open('test-data/concatenate/combined_evo.log', 'rt') as f:
            expected = f.read().splitlines()
        expected.append('')

        actual = buffer.getvalue().split('\n')

        self.assertEqual(expected, actual, "combined git history should be equivalent to concatenated content")

    def test_sort_combined_git_history_files(self):
        # SCENARIO Sort combined git history files
        parser = combine_repos.create_argument_parser()

        # GIVEN I have two git history files
        args = ["test-data/sort/first_evo.log", "test-data/sort/second_evo.log"]

        # WHEN I combine the git history files
        args = parser.parse_args(args)
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            combine_repos.run(args)

        # THEN the combined history is printed to stdout
        # AND the combined history is sorted by date in descending order
        with open('test-data/sort/combined_evo.log', 'rt') as f:
            expected = f.read().splitlines()
        expected.append('')

        actual = buffer.getvalue().split('\n')

        self.assertEqual(expected, actual, "combined git history should be sorted by date descending")

if __name__ == '__main__':
    unittest.main()
