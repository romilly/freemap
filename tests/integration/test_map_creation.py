import os

import datetime
import unittest

from hamcrest import is_not, none, starts_with
from hamcrest import assert_that, not_none, equal_to, contains_exactly

from freemap.map import Icons, Map
from freemap.helpers.files import read
from helpers.files import test_file


class TestMap(unittest.TestCase):
    def setUp(self):
        self.ts = 'CREATED="1541258689450" MODIFIED="1541353381000"'

    def test_reads_map(self):
        map_text = read(test_file('Mindmap.mm'))
        map = Map.from_string(map_text)
        assert_that(map, is_not(none()))
        root_node = map.root()
        assert_that(root_node.localized_text(), equal_to('new_mindmap'))

    def test_reads_root_node(self):
        mmap = Map.from_string('<map><node {ts}/></map>'.format(ts=self.ts))
        assert_that(mmap.root(), not_none())

    def test_uses_node_id_if_present(self):
        node_id = "Freemind_Link_1331878192"
        mmap = Map.from_string('<map><node ID="{nid}" {ts}/></map>'.format(nid=node_id, ts=self.ts))
        assert_that(mmap.root().node_id(), equal_to(node_id))

    def test_reads_branches(self):
        map__format = '<map><node {ts}><node {ts}/></node></map>'.format(ts=self.ts)
        mmap = Map.from_string(map__format)
        assert_that(len(mmap.root().branches()), equal_to(1))

    def test_reads_icons(self):
        mmap = Map.from_string('<map><node {ts}><icon BUILTIN="button_ok"/></node></map>'.format(ts=self.ts))
        assert_that(mmap.root().icons(), contains_exactly(Icons.icon('button_ok')))

    def test_reads_links(self):
        mmap = Map.from_string('<map><node {ts} LINK="foo"/></map>'.format(ts=self.ts))
        assert_that(mmap.root().link(), equal_to("foo"))

    def test_reads_notes(self):
        map_text = '<map><node {ts}><richcontent TYPE="NOTE"><html/></richcontent></node></map>'.format(ts=self.ts)
        mmap = Map.from_string(map_text)
        assert_that(mmap.root().note(), equal_to("<html/>"))

    def test_reads_branch_text(self):
        map_text = '<map><node {ts} TEXT="foo"><node {ts}/><node {ts} TEXT="bar"></node></node></map>' \
            .format(ts=self.ts)
        mmap = Map.from_string(map_text)
        assert_that((mmap.root().text()), equal_to("foo"))
        assert_that((mmap.root().branch(0).text()), none())
        assert_that((mmap.root().branch(1).text()), equal_to("bar"))

    def test_reads_timestamps(self):
        map_text = '<map><node {ts} TEXT="foo"><node></node><node {ts} TEXT="bar"></node></node></map>' \
            .format(ts=self.ts)
        mmap = Map.from_string(map_text)
        assert_that((mmap.root().created()), equal_to('1541258689450'))
        assert_that((mmap.root().modified()), equal_to('1541353381000'))

    def test_reads_node_with_markdown_text(self):
        map_text = read(test_file('test-plan.mm'))
        map = Map.from_string(map_text)
        assert_that(map, is_not(none()))
        root_node = map.root()
        assert_that(root_node.markdown_text(), starts_with('**test**\n\nplan'))

    def test_reads_node_with_details(self):
        map_text = read(test_file('test-plan.mm'))
        map = Map.from_string(map_text)
        root_node = map.root()
        assert_that(root_node.detail_markdown(), starts_with('plan details'))


if __name__ == '__main__':
    unittest.main()
