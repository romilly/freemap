import unittest
import datetime

from hamcrest import assert_that, not_none, equal_to, none, contains
from freemind.map import MapReader, Icons

__author__ = 'romilly'


class TestMapReader(unittest.TestCase):
    def test_reads_root_node(self):
            mmap = MapReader().read('<map><node/></map>')
            assert_that(mmap.root(), not_none())

    def test_genereates_node_id_if_missing(self):
        mmap = MapReader().read('<map><node/></map>')
        assert_that(mmap.root().id, not_none())

    def test_uses_node_id_if_present(self):
        id = "Freemind_Link_1331878192"
        mmap = MapReader().read('<map><node ID="%s"/></map>' % id)
        assert_that(mmap.root().id, equal_to(id))


    def test_reads_branches(self):
            mmap = MapReader().read('<map><node><node></node><icon BUILTIN="button_ok"/><node></node></node></map>')
            assert_that(len(mmap.root().branches()), equal_to(2))

    def test_reads_icons(self):
            mmap = MapReader().read('<map><node><node></node><icon BUILTIN="button_ok"/><node></node></node></map>')
            assert_that(mmap.root().icons(), contains(Icons.icon('button_ok')))

    def test_reads_links(self):
            mmap = MapReader().read('<map><node LINK="foo"><node></node><node></node></node></map>')
            assert_that(mmap.root().link(), equal_to("foo"))

    def test_reads_notes(self):
            mmap = MapReader().read('<map><node><richcontent TYPE="NOTE"><html/></richcontent></node></map>')
            assert_that(mmap.root().note(), equal_to("<html/>"))

    def test_reads_branch_text(self):
            mmap = MapReader().read('<map><node TEXT="foo"><node></node><node TEXT="bar"></node></node></map>')
            assert_that((mmap.root().text()), equal_to("foo"))
            assert_that((mmap.root().branch(0).text()), none())
            assert_that((mmap.root().branch(1).text()), equal_to("bar"))

    def test_reads_creation_timestamp(self):
            map_text = '<map><node TEXT="foo" CREATED="1541258689450"><node></node><node TEXT="bar"></node></node></map>'
            mmap = MapReader().read(map_text)
            assert_that((mmap.root().created), equal_to(datetime.datetime(2018,11,3,15,24,49,450000)))




