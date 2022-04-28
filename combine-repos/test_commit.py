import unittest
import ddt

from commit import Commit
from datetime import date

# TODO continue here: transform tests to data driven tests
@ddt.ddt
class CommitHistoryReaderDdtTest(unittest.TestCase):
    @ddt.data(
        '', None, 'Something without a date'
    )
    def test_given_first_line_when_date_then_returns_none(self, first_line):
        self.commit.first_line = first_line
        self.assertIsNone(self.commit.date)

class CommitHistoryReaderTest(unittest.TestCase):
    def setUp(self):
        self.commit = Commit()

    def test_given_empty_first_line_when_date_then_returns_none(self):
        self.assertIsNone(self.commit.date)

    def test_given_first_line_is_none_when_date_then_returns_none(self):
        self.commit.first_line = None
        self.assertIsNone(self.commit.date)

    def test_given_first_line_does_not_match_date_regex_when_date_then_returns_none(self):
        self.commit.first_line = 'Something without a date'
        self.assertIsNone(self.commit.date)

    def test_given_first_line_without_comment_after_date_when_date_then_returns_date(self):
        self.commit.first_line = 'Any prefix 2022-04-28'
        expected = date.fromisoformat('2022-04-28')
        self.assertEqual(expected, self.commit.date)

    def test_given_first_line_with_empty_author_when_date_then_returns_date(self):
        self.commit.first_line = '[1234567] 2022-04-28 Some comment'
        expected = date.fromisoformat('2022-04-28')
        self.assertEqual(expected, self.commit.date)
