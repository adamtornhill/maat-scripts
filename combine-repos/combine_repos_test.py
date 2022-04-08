import contextlib
import io
import unittest

import combine_repos


class CombineReposTest(unittest.TestCase):
    def test_should_work_in_progress(self):
        # build up an integration test step by step
        parser = combine_repos.create_argument_parser()

        # GIVEN I have two git history files
        args = ["test-data/first_evo.log", "test-data/second_evo.log"]

        # WHEN I combine the git history files
        args = parser.parse_args(args)
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            combine_repos.run(args)

        # THEN the combined history is printed to stdout
        with open('test-data/combined_evo.log', 'rt') as f:
            expected = f.read().splitlines()
        expected.append('')

        actual = buffer.getvalue().split('\n')

        self.assertEqual(expected, actual, "combined git history should be equivalent to concatenated content")


if __name__ == '__main__':
    unittest.main()
