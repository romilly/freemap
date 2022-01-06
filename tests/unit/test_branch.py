import unittest
from datetime import datetime as dt

from hamcrest import assert_that

from freemap.map import Branch
from helpers.matchers import between


class BranchTester(unittest.TestCase):
    def test_knows_when_created(self):
        before = round(1000*dt.now().timestamp())
        branch = Branch()
        after = round(1000*dt.now().timestamp())
        created = branch.created
        assert_that(float(created), between(before, after))

    def test_knows_when_attribute_modified(self):
        branch = Branch()
        t1 = round(1000*dt.now().timestamp())
        branch.set_link('foo')
        t2 = round(1000*dt.now().timestamp())
        assert_that(float(branch.modified), between(t1, t2))



