import unittest

from hamcrest import assert_that, equal_to, less_than, all_of, greater_than
from hamcrest.core.base_matcher import BaseMatcher

from freemind.map import Branch
from datetime import datetime as dt


class Between(BaseMatcher):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def _matches(self, item):
        return item >= self.low and  item <= self.high

    def describe_to(self, description):
        description.append('a value between %s and %s' % (self.low, self.high))


def between(low, high):
    return Between(low, high)


class BranchTester(unittest.TestCase):
    # def setUp(self):
    #     self.now = datetime(2018,11,10,1,2,3,456000) # constructor expects microseconds

    def test_knows_when_created(self):
        before = dt.now()
        self.branch = Branch('Any Id')
        after = dt.now()
        assert_that(self.branch.created(), between(before, after))

    # def test_knows_when_core_attribute_modified(self):
    #     assert_that(self.branch.modified(), equal_to(self.now))
    #     test_time = datetime.now()
    #     self.branch.set_text('foo')
    #     td = self.branch.modified() - test_time
    #     assert_that(abs(td), less_than(timedelta(milliseconds=10)))

