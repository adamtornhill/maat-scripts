import unittest
from commit_history_reader import CommitHistoryReader
from commit import Commit


class CommitHistoryReaderTest(unittest.TestCase):
    def test_given_empty_file_when_parse_then_return_no_commit(self):
        file_contents = ''
        commits = CommitHistoryReader().parse(file_contents)
        self.assertEqual(len(commits), 0)

    def test_given_one_commit_in_file_when_parse_then_return_single_commit(self):
        contents = '[1234567] Commit Message\n' \
                   '1\t2\tfilename'
        commits = CommitHistoryReader().parse(contents)

        expected = Commit()
        expected.first_line = '[1234567] Commit Message'
        expected.change_lines = ['1\t2\tfilename']

        self.assertEqual([expected], commits)

    def test_given_two_commits_in_file_when_parse_then_return_two_commits(self):
        contents = '[1234567] First Commit Message\n' \
                   '1\t2\tfirst\n' \
                   '\n' \
                   '[1234567] Second Commit Message\n' \
                   '3\t4\tsecond\n'
        commits = CommitHistoryReader().parse(contents)

        expected = [Commit()]
        expected[0].first_line = '[1234567] First Commit Message'
        expected[0].change_lines = ['1\t2\tfirst']

        expected.append(Commit())
        expected[1].first_line = '[1234567] Second Commit Message'
        expected[1].change_lines = ['3\t4\tsecond']

        self.assertEqual(expected, commits)


if __name__ == '__main__':
    unittest.main()
