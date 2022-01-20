import unittest
from datetime import datetime as dt
from time import sleep

from hamcrest import assert_that, equal_to, contains_exactly

from freemap.map import Branch, Icons, Map
from helpers.matchers import between


class BranchTester(unittest.TestCase):
    def setUp(self):
        self.ts = 'CREATED="1541258689450" MODIFIED="1541353381000"'
        self.branch_with_text = Branch.for_tests_from_string('<node TEXT="text"/>')
        self.branch_with_localized_text = Branch.for_tests_from_string('<node LOCALIZED_TEXT="localized"/>')
        self.branch_with_rich_content = Branch.for_tests_from_string(
            '<node><richcontent TYPE="NODE"><html><body><p>Ha!</p></body></html></richcontent></node>')
        self.branch_with_note = Branch.for_tests_from_string(
            '<node><richcontent TYPE="NOTE"><html><body><p>Hi!</p></body></html></richcontent></node>')
        self.branch_with_details = Branch.for_tests_from_string('<node><richcontent '
                                    'TYPE="DETAILS"><html><body><p>Who!</p></body></html></richcontent></node>')
        self.branch_with_icons = Branch.for_tests_from_string('<node><icon BUILTIN="button_ok"/><icon BUILTIN="full-1"/></node>')

    def test_knows_when_created(self):
        before = self.now()
        branch = Branch(Map())
        after = self.now()
        created = branch.created
        assert_that(created, between(before, after))

    def test_uses_node_id_if_present(self):
        node_id = "Freemind_Link_1331878192"
        branch = Branch.for_tests_from_string('<node ID="{nid}" {ts}/>'.format(nid=node_id, ts=self.ts))
        assert_that(branch.node_id, equal_to(node_id))

    def test_knows_when_attribute_modified(self):
        branch = Branch(Map())
        t1 = self.now()
        branch.set_link('foo')
        t2 = self.now()
        assert_that(branch.modified, between(t1, t2))

    def test_knows_when_child_added(self):
        mmap = Map()
        branch = Branch(mmap)
        t1 = branch.modified
        sleep(0.01)
        branch.add_child(Branch(mmap))
        t2 = branch.modified
        assert_that(t1 < t2)

    def now(self):
        return round(1000 * dt.now().timestamp())

    def test_knows_timestamps(self):
        text = '<node {ts} TEXT="foo"></node>' \
            .format(ts=self.ts)
        branch = Branch.for_tests_from_string(text)
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
        assert_that(self.branch_with_note.note.markdown, equal_to('Hi!'))

    def test_can_set_note(self):
        self.branch_with_text.note = 'Note one'
        assert_that(self.branch_with_text.note.markdown, equal_to('Note one'))
        self.branch_with_note.note = 'replacement note'
        assert_that(self.branch_with_note.note.markdown, equal_to('replacement note'))


    def test_retrieves_description(self):
        assert_that(self.branch_with_details.details.markdown, equal_to('Who!'))

    def test_sets_details(self):
        self.branch_with_text.details = 'interesting details'
        assert_that(self.branch_with_text.details.markdown, equal_to('interesting details'))

    def test_retrieves_link(self):
        branch = Branch.for_tests_from_string('<node LINK="foo"/>')
        assert_that(branch.link, equal_to('foo'))

    def test_sets_link(self):
        branch = Branch.for_tests_from_string('<node LINK="foo"/>')
        branch.link = 'boo!'
        assert_that(branch.link, equal_to('boo!'))

    def test_reads_icons(self):
        assert_that(self.branch_with_icons.icons, contains_exactly(Icons.icon('button_ok'),Icons.icon('full-1')))

    def test_adds_icons(self):
        self.branch_with_icons.add_icons(Icons.icon('full-2'))
        assert_that(self.branch_with_icons.icons, contains_exactly(
            Icons.icon('button_ok'),
            Icons.icon('full-1'),
            Icons.icon('full-2')))

    def test_removes_icons(self):
        self.branch_with_icons.remove_icons(Icons.icon('button_ok'), Icons.icon('full-1'))
        assert_that(len(self.branch_with_icons.icons), equal_to(0))








