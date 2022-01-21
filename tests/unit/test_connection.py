import unittest

from hamcrest import assert_that, not_none, equal_to

from freemap.helpers.base_connection import arrowlink
from freemap.map import Connection


class ConnectionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = Connection.for_tests_from_string(None, arrowlink)

    def test_can_create_connection(self):
        assert_that(self.connection, not_none())

    def test_knows_labels(self):
        assert_that(self.connection.source_label, equal_to('source'))
        assert_that(self.connection.middle_label, equal_to('middle'))
        assert_that(self.connection.target_label, equal_to('target'))

    def test_sets_labels(self):
        self.connection.source_label = 'foo'
        self.connection.middle_label = 'bar'
        self.connection.target_label = 'baz'
        assert_that(self.connection.source_label, equal_to('foo'))
        assert_that(self.connection.middle_label, equal_to('bar'))
        assert_that(self.connection.target_label, equal_to('baz'))

    def test_knows_inclinations(self):
        assert_that(self.connection.start_inclination, equal_to('136;0;'))
        assert_that(self.connection.end_inclination, equal_to('147;0;'))

    def test_sets_inclinations(self):
        self.connection.start_inclination = '0;45;'
        self.connection.end_inclination = '0;135;'
        assert_that(self.connection.start_inclination, equal_to('0;45;'))
        assert_that(self.connection.end_inclination, equal_to('0;135;'))


if __name__ == '__main__':
    unittest.main()
