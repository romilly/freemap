import unittest

from hamcrest import assert_that, not_none, equal_to, contains_exactly
from hamcrest import is_not, none, starts_with

from freemap.helpers.files import read
from freemap.map import Icons, Map
from helpers.files import test_file

#TODO: separate unit tests (building from text)  and integration tests (building from file)
#TODO: add integration tests for link, icons, note, description,text (all three forms)
# as this checks that we are testing against actual formats.
#TODO: remove or move map unit tests that should test at the branch level.

class TestMap(unittest.TestCase):
    def setUp(self):
        self.ts = 'CREATED="1541258689450" MODIFIED="1541353381000"'

    def test_reads_map(self):
        map_text = read(test_file('Mindmap.mm'))
        map = Map.from_string(map_text)
        assert_that(map, is_not(none()))
        root_node = map.root()
        assert_that(root_node.text, equal_to('new_mindmap'))

    def test_reads_node_with_markdown_text(self):
        map_text = read(test_file('test-plan.mm'))
        map = Map.from_string(map_text)
        assert_that(map, is_not(none()))
        root_node = map.root()
        assert_that(root_node.text, starts_with('**test**\n\nplan'))

    def test_reads_node_with_details(self):
        map_text = read(test_file('test-plan.mm'))
        map = Map.from_string(map_text)
        root_node = map.root()
        assert_that(root_node.details.markdown, starts_with('plan details'))


if __name__ == '__main__':
    unittest.main()
