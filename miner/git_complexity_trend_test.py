import unittest
import argparse

import git_complexity_trend


class GitComplexityTrendTest(unittest.TestCase):
    def test_git_complexity_trend_should_process_file_under_test(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--start')
        parser.add_argument('--end')
        parser.add_argument('--file')

        args = list(["--start", "89272ea", "--end", "30b449a", "--file", "./git_complexity_trend.py"])
        args = parser.parse_args(args)

        git_complexity_trend.run(args)
        self.assertTrue(True, "Test should pass without throwing an error.")


if __name__ == '__main__':
    unittest.main()
