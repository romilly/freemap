import datetime
import unittest

from hamcrest import assert_that, not_none, equal_to, contains_exactly

from freemap.map import Icons
from freemap.reader import MapReader

__author__ = 'romilly'


class TestMapReader(unittest.TestCase):
    def setUp(self):
        self.ts = 'CREATED="1541258689450" MODIFIED="1541353381000"'

    def test_reads_root_node(self):
            mmap = MapReader().read('<map><node {ts}/></map>'.format(ts=self.ts))
            assert_that(mmap.root(), not_none())

    def test_generates_node_id_if_missing(self):
        mmap = MapReader().read('<map><node {ts}/></map>'.format(ts=self.ts))
        assert_that(mmap.root().id, not_none())

    def test_uses_node_id_if_present(self):
        node_id = "Freemind_Link_1331878192"
        mmap = MapReader().read('<map><node ID="{nid}" {ts}/></map>'.format(nid=node_id, ts=self.ts))
        assert_that(mmap.root().id, equal_to(node_id))


    def test_reads_branches(self):
            map__format = '<map><node {ts}><node {ts}/></node></map>'.format(ts=self.ts)
            mmap = MapReader().read(map__format)
            assert_that(len(mmap.root().branches()), equal_to(1))

    def test_reads_icons(self):
            mmap = MapReader().read('<map><node {ts}><icon BUILTIN="button_ok"/></node></map>'.format(ts=self.ts))
            assert_that(mmap.root().icons(), contains_exactly(Icons.icon('button_ok')))

    def test_reads_links(self):
            mmap = MapReader().read('<map><node {ts} LINK="foo"/></map>'.format(ts=self.ts))
            assert_that(mmap.root().link(), equal_to("foo"))

    def test_reads_notes(self):
            map_text = '<map><node {ts}><richcontent TYPE="NOTE"><html/></richcontent></node></map>'.format(ts=self.ts)
            mmap = MapReader().read(map_text)
            assert_that(mmap.root().note(), equal_to("<html/>"))

    def test_reads_branch_text(self):
            map_text = '<map><node {ts} TEXT="foo"><node {ts}/><node {ts} TEXT="bar"></node></node></map>'\
                .format(ts=self.ts)
            mmap = MapReader().read(map_text)
            assert_that((mmap.root().text()), equal_to("foo"))
            assert_that((mmap.root().branch(0).text()), equal_to(""))
            assert_that((mmap.root().branch(1).text()), equal_to("bar"))

    def test_reads_timestamps(self):
            map_text = '<map><node {ts} TEXT="foo"><node></node><node {ts} TEXT="bar"></node></node></map>'\
                .format(ts=self.ts)
            mmap = MapReader().read(map_text)
            assert_that((mmap.root().created()), equal_to(datetime.datetime(2018,11,3,15,24,49,450000)))
            assert_that((mmap.root().modified()), equal_to(datetime.datetime(2018,11,4,17,43,1,0)))


    # def test_reads_links(self):




