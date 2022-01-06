import unittest
from datetime import datetime as dt

from hamcrest import assert_that
from hamcrest.core.base_matcher import BaseMatcher

from freemap.map import Branch, Icons


class Between(BaseMatcher):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def _matches(self, item):
        return self.low <= item <= self.high

    def describe_to(self, description):
        description.append_text('a value between %s and %s' % (self.low, self.high))


def between(low, high):
    return Between(low, high)


class BranchTester(unittest.TestCase):
    def test_knows_when_created(self):
        before = round(1000*dt.now().timestamp())
        branch = Branch()
        after = round(1000*dt.now().timestamp())
        created = branch.created()
        assert_that(float(created), between(before, after))

    def test_knows_when_attribute_modified(self):
        branch = Branch()
        t1 = round(1000*dt.now().timestamp())
        branch.set_link('foo')
        t2 = round(1000*dt.now().timestamp())
        assert_that(float(branch.modified), between(t1, t2))



