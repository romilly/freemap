import unittest
from datetime import datetime as dt

from hamcrest import assert_that, equal_to

from freemap.map import Branch
from helpers.matchers import between


class BranchTester(unittest.TestCase):
    def test_knows_when_created(self):
        before = round(1000*dt.now().timestamp())
        branch = Branch()
        after = round(1000*dt.now().timestamp())
        created = branch.created
        assert_that(created, between(before, after))

    def test_knows_when_attribute_modified(self):
        branch = Branch()
        t1 = round(1000*dt.now().timestamp())
        branch.set_link('foo')
        t2 = round(1000*dt.now().timestamp())
        assert_that(branch.modified, between(t1, t2))

    def test_retrieves_rich_text(self):
        branch = Branch.from_string('<node><richcontent '
                                    'TYPE="NODE"><html><body><p>Ha!</p></body></html></richcontent></node>')
        assert_that(branch.text, equal_to('Ha!'))

    def test_retrieves_note(self):
        branch = Branch.from_string('<node><richcontent '
                                    'TYPE="NOTE"><html><body><p>Hi!</p></body></html></richcontent></node>')
        assert_that(branch.note, equal_to('Hi!'))

    def test_retrieves_description(self):
        branch = Branch.from_string('<node><richcontent '
                                    'TYPE="DETAILS"><html><body><p>Who!</p></body></html></richcontent></node>')
        assert_that(branch.details, equal_to('Who!'))





