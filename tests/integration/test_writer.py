import unittest

from hamcrest import assert_that

from freemap.helpers.files import read, write
from freemap.map import Map
from helpers.files import test_file, xml_equal


class WriterTestCase(unittest.TestCase):
        def test_writes_map_as_read(self):
            test_in = 'test-plan.mm'
            map_text = read(test_file(test_in))
            mmap = Map.from_string(map_text)
            test_out = 'test_plan_out.mm'
            write(mmap.as_text(), test_file(test_out))
            assert_that(xml_equal(test_in, test_out))




if __name__ == '__main__':
    unittest.main()
