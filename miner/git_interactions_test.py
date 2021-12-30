import unittest
import subprocess
import git_interactions


class GitInteractionsTest(unittest.TestCase):
    def test_split_subprocess_stdout_using_utf8_encoded_linefeed(self):
        """ Verify the assumption that subprocess.Popen returns stdout as UTF-8 encoded byte array
        """
        process_stdout = subprocess.Popen(["echo", "first line\nsecond line"], stdout=subprocess.PIPE).communicate()[0]

        lines = process_stdout.split('\n'.encode('UTF-8'))

        self.assertEqual(3, len(lines))

    def test_read_revisions_matching_should_return_three_revisions(self):
        expected_revision = "d804759"
        fake_git_result = expected_revision + " Documented tree map visualizations"
        fake_git_cmd = ['echo', fake_git_result]

        actual = git_interactions._read_revisions_matching(fake_git_cmd)

        self.assertEqual([expected_revision], actual)


if __name__ == '__main__':
    unittest.main()
