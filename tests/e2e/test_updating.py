import unittest

from freemap.helpers.files import write
from freemap.map import Map
from helpers.files import test_file, assert_xml_equal


class UpdatingTestCase(unittest.TestCase):
    def test_writes_map(self):
        expected = test_file('test-1-expected.mm')
        mmap = Map()
        actual = test_file('output/test-1-actual.mm')
        write(mmap.as_text(), actual)
        assert_xml_equal(expected, actual)

    def test_updates_root_text(self):
        expected = test_file('test-2-expected.mm')
        mmap = Map()
        mmap.root().set_text('Wow!')
        actual = test_file('output/test-2-actual.mm')
        write(mmap.as_text(), actual)
        assert_xml_equal(expected, actual)


if __name__ == '__main__':
    unittest.main()
