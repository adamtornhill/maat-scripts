import unittest
import argparse
import io
import contextlib

import git_complexity_trend


class GitComplexityTrendTest(unittest.TestCase):
    def test_git_complexity_trend_should_process_file_under_test(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--start')
        parser.add_argument('--end')
        parser.add_argument('--file')

        # GIVEN the file ./git_complexity_trend.py with commit history
        #       30b449a Clean out obsolete imports
        #       89272ea Moved the complexity calculations into their own module
        #       7ad7fee Scripts to analyze omplexity trends
        #       (as shown by "git log ./git_complexity_trend.py")

        # WHEN the git complexity trend is analyzed between first and third commit
        #      (note that "git log" excludes the first revision from the analysis,
        #      see https://git-scm.com/docs/gitrevisions#_specifying_ranges)
        args = list(["--start", "7ad7fee1", "--end", "30b449a", "--file", "./git_complexity_trend.py"])
        args = parser.parse_args(args)

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            git_complexity_trend.run(args)

        # THEN the result printed to stdout is
        #      rev,n,total,mean,sd
        #      89272ea,47,29.0,0.62,0.7
        #      30b449a,46,29.0,0.63,0.7
        #      (including the line generated from splitting the stdout output by linefeed)
        expected = ["rev,n,total,mean,sd",
                    "89272ea,47,29.0,0.62,0.7",
                    "30b449a,46,29.0,0.63,0.7",
                    '']
        actual = buffer.getvalue().split("\n")
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
