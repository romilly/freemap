import unittest
from datetime import datetime as dt

from hamcrest import assert_that, equal_to, contains_exactly

from freemap.map import Branch, Icons
from helpers.matchers import between


class BranchTester(unittest.TestCase):
    def setUp(self):
        self.ts = 'CREATED="1541258689450" MODIFIED="1541353381000"'
        self.branch_with_text = Branch.from_string('<node TEXT="text"/>')
        self.branch_with_localized_text = Branch.from_string('<node LOCALIZED_TEXT="localized"/>')
        self.branch_with_rich_content = Branch.from_string(
            '<node><richcontent TYPE="NODE"><html><body><p>Ha!</p></body></html></richcontent></node>')

    def test_knows_when_created(self):
        before = self.now()
        branch = Branch()
        after = self.now()
        created = branch.created
        assert_that(created, between(before, after))

    def test_uses_node_id_if_present(self):
        node_id = "Freemind_Link_1331878192"
        branch = Branch.from_string('<node ID="{nid}" {ts}/>'.format(nid=node_id, ts=self.ts))
        assert_that(branch.node_id, equal_to(node_id))

    def test_knows_when_attribute_modified(self):
        branch = Branch()
        t1 = self.now()
        branch.set_link('foo')
        t2 = self.now()
        assert_that(branch.modified, between(t1, t2))

    def now(self):
        return round(1000 * dt.now().timestamp())

    def test_knows_timestamps(self):
        text = '<node {ts} TEXT="foo"></node>' \
            .format(ts=self.ts)
        branch = Branch.from_string(text)
        assert_that(branch.created, equal_to(1541258689450))
        assert_that(branch.modified, equal_to(1541353381000))

    def test_knows_if_text_is_rich(self):
        assert_that(self.branch_with_rich_content.has_rich_content())
        assert_that(not self.branch_with_text.has_rich_content())
        assert_that(not self.branch_with_localized_text.has_rich_content())

    def test_retrieves_text_from_rich_content_nodes(self):
        assert_that(self.branch_with_rich_content.text, equal_to('Ha!'))

    def test_sets_text(self):
        self.branch_with_text.text = 'Foo'
        assert_that(self.branch_with_text.text, equal_to('Foo'))
        self.branch_with_localized_text.text = 'Bar'
        assert_that(self.branch_with_localized_text.text, equal_to('Bar'))
        self.branch_with_rich_content.text = 'Baz'
        assert_that(self.branch_with_rich_content.text, equal_to('Baz'))

    def test_retrieves_rich_content_from_nodes(self):
        assert_that(self.branch_with_text.rich_content.markdown, equal_to('text'))
        assert_that(self.branch_with_localized_text.rich_content.markdown, equal_to('localized'))
        assert_that(self.branch_with_rich_content.rich_content.markdown, equal_to('Ha!'))

    def test_sets_rich_content(self):
        self.branch_with_rich_content.rich_content = 'Ho!'
        assert_that(self.branch_with_rich_content.rich_content.markdown, equal_to('Ho!'))
        self.branch_with_text.rich_content = 'Hi!'
        assert_that(self.branch_with_text.rich_content.markdown, equal_to('Hi!'))
        self.branch_with_localized_text.rich_content = 'Hum!'
        assert_that(self.branch_with_localized_text.rich_content.markdown, equal_to('Hum!'))

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
        assert_that(branch.icons, contains_exactly(Icons.icon('button_ok')))








