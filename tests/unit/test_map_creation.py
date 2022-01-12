import unittest

from hamcrest import assert_that, not_none, equal_to

from freemap.map import Map

MAP_TEXT = '<map><node ID="1" TEXT="One"><node ID="2" TEXT="Two"/><node ID="3" TEXT="Three"></node><node/></node></map>'


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
        mmap = Map.from_string(MAP_TEXT)
        root = mmap.root()
        assert_that(root.node_id, equal_to('1'))
        assert_that((root.branch(0).node_id), equal_to('2'))
        assert_that((root.branch(1).node_id), equal_to('3'))

    def test_finds_branch_by_id(self):
        mmap = Map.from_string(MAP_TEXT)
        ids = [str(i+1) for i in range(3)]
        texts = ['One','Two','Three']
        branches = [mmap.branch_with_id(node_id) for node_id in ids]
        for (branch, text) in zip(branches, texts):
            assert_that(branch.text, equal_to(text))


if __name__ == '__main__':
    unittest.main()
