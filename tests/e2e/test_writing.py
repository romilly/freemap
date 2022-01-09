import unittest

from freemap.helpers.files import read, write
from freemap.map import Map
from helpers.files import test_file, assert_xml_equal


class WritingTestCase(unittest.TestCase):
        def test_writes_map_as_read(self):
            test_in = test_file('test-plan.mm')
            map_text = read(test_in)
            mmap = Map.from_string(map_text)
            test_out = test_file('output/test_plan_out.mm')
            write(mmap.as_text(), test_out)
            assert_xml_equal(test_in, test_out, ignore_timestamps=False)




if __name__ == '__main__':
    unittest.main()
