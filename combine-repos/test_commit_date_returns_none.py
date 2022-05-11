import unittest

import ddt

from commit import Commit


@ddt.ddt
class CommitDateReturnsNoneTest(unittest.TestCase):
    def setUp(self):
        self.commit = Commit()

    @ddt.data(
        '', None, 'Something without a date'
    )
    def test(self, first_line):
        self.commit.first_line = first_line
        self.assertIsNone(self.commit.date)
