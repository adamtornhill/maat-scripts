import re
import unittest
import argparse
import io
import contextlib

import complexity_analysis


class ComplexityAnalysisTest(unittest.TestCase):
    def test_complexity_analysis_should_process_non_utf8_encoded_files(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('file')

        args = list(["./test-data/iso8859-1-encoded-test-file-with-umlauts.txt"])
        args = parser.parse_args(args)

        try:
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                complexity_analysis.run(args)
        except:
            self.fail('complexity_analysis.run fails for iso-8859-1 encoded files')

        self.assertContainsCsvData(buffer)

    def assertContainsCsvData(self, buffer):
        # Sample data:
        # n,total,mean,sd,max
        # 26,40.0,1.54,1.22,4.0
        expected_regex = re.compile(
            '^n,total,mean,sd,max$\n^[0-9]+,[0-9.]+,[0-9.]+,[0-9.]+,[0-9.]+$',
            flags=re.MULTILINE)
        self.assertRegex(buffer.getvalue(), expected_regex, 'complexity_analysis.run() should print csv data')


if __name__ == '__main__':
    unittest.main()
