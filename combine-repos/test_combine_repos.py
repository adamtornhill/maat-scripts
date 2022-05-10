import os
import tempfile
import unittest

import combine_repos
from capture_stdout_to_list import CaptureStdoutToList


class TestCase:
    def __init__(self, t, description, input_history_files, expected_history_file):
        self.t = t
        self.input_history_files = input_history_files
        self.expected_history_file = expected_history_file
        self.description = description

    def run(self):
        parser = combine_repos.create_argument_parser()

        # GIVEN I have a number of git history files
        args = self.input_history_files

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
            TestCase(self, "2 input files with 1 commit per file => simply concatenate the files",
                     [
                         "test-data/concatenate_2_files/first_evo.log",
                         "test-data/concatenate_2_files/second_evo.log",
                     ],
                     "test-data/concatenate_2_files/combined_evo.log"),

            TestCase(self, "3 input files with 1 commit per file => simply concatenate the files",
                     [
                         "test-data/concatenate_3_files/first_evo.log",
                         "test-data/concatenate_3_files/second_evo.log",
                         "test-data/concatenate_3_files/third_evo.log"
                     ],
                     "test-data/concatenate_3_files/combined_evo.log"),

            TestCase(self, "multiple commits per file => result is sorted by date descending",
                     ["test-data/sort/first_evo.log", "test-data/sort/second_evo.log"],
                     "test-data/sort/combined_evo.log"),

            TestCase(self, "merge commits and ordinary commits => sorting rearranges both commit types",
                     ["test-data/merge-commits/first_evo.log", "test-data/merge-commits/second_evo.log"],
                     "test-data/merge-commits/combined_evo.log")
        ]

        self.maxDiff = None
        for case in suite:
            with self.subTest(case.description):
                case.run()

    def test_output_parameter(self):
        parser = combine_repos.create_argument_parser()

        with tempfile.TemporaryDirectory() as tempdirname:
            outfilepath = os.path.join(tempdirname, "combined_evo.log")

            # GIVEN I have two git history files
            args = ["test-data/concatenate_2_files/first_evo.log", "test-data/concatenate_2_files/second_evo.log"]

            # AND I specify an outfile
            args += ["--output", outfilepath]

            # WHEN I combine the git history files
            args = parser.parse_args(args)
            combine_repos.run(args)

            # THEN the outfile exists and is not empty
            outfilestat = os.stat(outfilepath)
            self.assertTrue(outfilestat.st_size > 0, 'outfile should exist and have size > 0')


if __name__ == '__main__':
    unittest.main()
