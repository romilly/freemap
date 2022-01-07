import unittest

from hamcrest import assert_that, not_none, equal_to

from freemap.map import Map


#TODO: remove or move map unit tests that should test at the branch level.

class TestMap(unittest.TestCase):
    def setUp(self):
        self.ts = 'CREATED="1541258689450" MODIFIED="1541353381000"'

    def test_reads_root_node(self):
        mmap = Map.from_string('<map><node/></map>')
        assert_that(mmap.root(), not_none())

    def test_reads_branch(self):
        map__format = '<map><node><node/></node></map>'
        mmap = Map.from_string(map__format)
        assert_that(len(mmap.root().branches()), equal_to(1))

    def test_reads_nested_branches(self):
        map_text = '<map><node ID="1"><node ID="2"/><node ID="3"></node></node></map>'
        mmap = Map.from_string(map_text)
        root = mmap.root()
        assert_that(root.node_id, equal_to('1'))
        assert_that((root.branch(0).node_id), equal_to('2'))
        assert_that((root.branch(1).node_id), equal_to('3'))



if __name__ == '__main__':
    unittest.main()
