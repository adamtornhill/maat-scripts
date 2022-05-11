import unittest
import ddt

from commit import Commit
from datetime import date


@ddt.ddt
class CommitDateReturnsValidDateTest(unittest.TestCase):
    def setUp(self):
        self.commit = Commit()

    @ddt.data(
        'No Comment 2022-04-28', '[1234567] 2022-04-28 No Author'
    )
    def test(self, first_line):
        self.commit.first_line = first_line
        expected = date.fromisoformat('2022-04-28')
        self.assertEqual(expected, self.commit.date)

