import unittest
import combine_repos
from capture_stdout_to_list import CaptureStdoutToList

class TestCase:
    def __init__(self, t, description, first_history_file, second_history_file, expected_history_file):
        self.t = t
        self.first_history_file = first_history_file
        self.second_history_file = second_history_file
        self.expected_history_file = expected_history_file
        self.description = description

    def run(self):
        parser = combine_repos.create_argument_parser()

        # GIVEN I have two git history files
        args = [self.first_history_file, self.second_history_file]

        # WHEN I combine the git history files
        args = parser.parse_args(args)
        actual = []
        with CaptureStdoutToList(actual):
            combine_repos.run(args)

        # THEN the combined history is printed to stdout
        # AND the combined history matches the expected file
        with open(self.expected_history_file, 'rt') as f:
            expected = f.read().splitlines()

        self.t.assertEqual(expected, actual, self.description)


class CombineReposTest(unittest.TestCase):
    def test_suite(self):
        suite = [
            TestCase(self, "1 commit per file => simply concatenate the files",
                     "test-data/concatenate/first_evo.log", "test-data/concatenate/second_evo.log",
                     "test-data/concatenate/combined_evo.log"),

            # TODO Implement the following feature and enable the corresponding test
            #TestCase(self, "multiple commits per file => result is sorted by date descending",
            #         "test-data/sort/first_evo.log", "test-data/sort/second_evo.log",
            #         "test-data/sort/combined_evo.log")
        ]

        for case in suite:
            with self.subTest(case.description):
                case.run()


if __name__ == '__main__':
    unittest.main()
