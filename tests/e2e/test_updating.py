import unittest

from hamcrest import assert_that

from freemap.helpers.files import write
from freemap.map import Map
from helpers.files import test_file, xml_equal


class UpdatingTestCase(unittest.TestCase):
    def test_writes_map(self):
        expected = test_file('test-1-expected.mm')
        mmap = Map()
        actual = test_file('test-1-actual.mm')
        write(mmap.as_text(), actual)
        assert_that(xml_equal(expected, actual))

if __name__ == '__main__':
    unittest.main()
