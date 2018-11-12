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

    def test_knows_when_created(self):
        before = dt.now()
        branch = Branch('Any Id')
        after = dt.now()
        assert_that(branch.created(), between(before, after))

    def test_knows_when_text_modified(self):
        branch = Branch('Any Id')
        before = dt.now()
        branch.set_text('foo')
        after = dt.now()
        assert_that(branch.modified(), between(before, after))



