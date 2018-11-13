import unittest

from hamcrest import assert_that, equal_to, less_than, all_of, greater_than
from hamcrest.core.base_matcher import BaseMatcher

from freemind.map import Branch, Icon, Icons
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

    def test_knows_when_attribute_modified(self):
        branch = Branch('Any Id')
        t1 = dt.now()
        branch.set_link('foo')
        t2 = dt.now()
        assert_that(branch.modified(), between(t1, t2))
        branch.set_icons([Icons.icon('foo')])
        t3 = dt.now()
        assert_that(branch.modified(), between(t2, t3))
        branch.set_note('bar')
        t4 = dt.now()
        assert_that(branch.modified(), between(t3, t4))



