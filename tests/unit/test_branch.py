import unittest
from datetime import datetime as dt

from hamcrest import assert_that, equal_to, contains_exactly

from freemap.map import Branch, Icons
from helpers.matchers import between

# TODO: add tests for TEXT, LOCALISED_TEXT

class BranchTester(unittest.TestCase):
    def setUp(self):
        self.ts = 'CREATED="1541258689450" MODIFIED="1541353381000"'

    def test_knows_when_created(self):
        before = round(1000*dt.now().timestamp())
        branch = Branch()
        after = round(1000*dt.now().timestamp())
        created = branch.created
        assert_that(created, between(before, after))

    def test_uses_node_id_if_present(self):
        node_id = "Freemind_Link_1331878192"
        branch = Branch.from_string('<node ID="{nid}" {ts}/>'.format(nid=node_id, ts=self.ts))
        assert_that(branch.node_id, equal_to(node_id))

    def test_knows_when_attribute_modified(self):
        branch = Branch()
        t1 = round(1000*dt.now().timestamp())
        branch.set_link('foo')
        t2 = round(1000*dt.now().timestamp())
        assert_that(branch.modified, between(t1, t2))

    def test_knows_timestamps(self):
        text = '<node {ts} TEXT="foo"></node>' \
            .format(ts=self.ts)
        branch = Branch.from_string(text)
        assert_that(branch.created, equal_to(1541258689450))
        assert_that(branch.modified, equal_to(1541353381000))

    def test_retrieves_rich_text(self):
        branch = Branch.from_string('<node><richcontent '
                                    'TYPE="NODE"><html><body><p>Ha!</p></body></html></richcontent></node>')
        assert_that(branch.text.markdown, equal_to('Ha!'))

    def test_retrieves_note(self):
        branch = Branch.from_string('<node><richcontent '
                                    'TYPE="NOTE"><html><body><p>Hi!</p></body></html></richcontent></node>')
        assert_that(branch.note.markdown, equal_to('Hi!'))

    def test_retrieves_description(self):
        branch = Branch.from_string('<node><richcontent '
                                    'TYPE="DETAILS"><html><body><p>Who!</p></body></html></richcontent></node>')
        assert_that(branch.details.markdown, equal_to('Who!'))

    def test_retrieves_link(self):
        branch = Branch.from_string('<node LINK="foo"/>')
        assert_that(branch.link, equal_to('foo'))

    def test_sets_link(self):
        branch = Branch.from_string('<node LINK="foo"/>')
        branch.link = 'boo!'
        assert_that(branch.link, equal_to('boo!'))

    def test_reads_icons(self):
        branch = Branch.from_string('<node><icon BUILTIN="button_ok"/></node>')
        assert_that(branch.icons(), contains_exactly(Icons.icon('button_ok')))








