import unittest

from hamcrest import assert_that, equal_to

from freemap.map import Map


class MapUpdateTestCase(unittest.TestCase):
    def test_updates_text(self):
        mmap = Map()
        mmap.root().set_text('Wow!')
        assert_that(mmap.root().text(), equal_to('Wow!'))


if __name__ == '__main__':
    unittest.main()
