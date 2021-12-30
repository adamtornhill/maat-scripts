import unittest
import subprocess


class GitInteractionsTest(unittest.TestCase):
    def test_split_subprocess_stdout_using_utf8_encoded_linefeed(self):
        """ Verify the assumption that subprocess.Popen returns stdout as UTF-8 encoded byte array
        """
        process_stdout = subprocess.Popen(["echo", "first line\nsecond line"], stdout=subprocess.PIPE).communicate()[0]

        lines = process_stdout.split("\n".encode('UTF-8'))

        self.assertEqual(3, len(lines))


if __name__ == '__main__':
    unittest.main()
