import polling_unit_lookup
import unittest
import requests_mock


class PollingUnitLookupTestCase(unittest.TestCase):

    def setUp(self):
        polling_unit_lookup.app.config['TESTING'] = True
        polling_unit_lookup.app.config['MAPIT_API_URL'] = 'http://pmo'
        polling_unit_lookup.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        self.app = polling_unit_lookup.app.test_client()

    def test_polling_unit_lookup_invalid_number(self):
        rv = self.app.get('/?lookup=abcd')
        assert 'Unrecognized polling unit: abcd' in rv.data
        self.assertEqual(rv.status_code, 404)

    def test_polling_unit_lookup_valid_number(self):
        with requests_mock.mock() as m:
            m.get('http://pmo/code/poll_unit/AB:1:23:45', text='{"name": "Area"}')
            rv = self.app.get('/?lookup=AB%3A01%3A23%3A45')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.data, '{"name": "Area"}')

    def test_polling_unit_lookup_valid_number_no_area(self):
        with requests_mock.mock() as m:
            m.get('http://pmo/code/poll_unit/ZZ', status_code=404)
            rv = self.app.get('/?lookup=ZZ')
            self.assertEqual(rv.status_code, 404)
            assert 'No areas were found that matched polling unit: ZZ' in rv.data

    def test_lookup_tries_multiple_variations(self):
        with requests_mock.mock() as m:
            m.get('http://pmo/code/poll_unit/AB:1:23:45', status_code=404)
            m.get('http://pmo/code/poll_unit/AB:1:23', status_code=404)
            m.get('http://pmo/code/poll_unit/AB:1', status_code=404)
            m.get('http://pmo/code/poll_unit/AB', text='{"name": "Area"}')
            rv = self.app.get('/?lookup=AB%3A01%3A23%3A45')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.data, '{"name": "Area"}')

    def test_lookup_with_slashes(self):
        with requests_mock.mock() as m:
            m.get('http://pmo/code/poll_unit/AB:2:3:4', text='{"name": "Area"}')
            rv = self.app.get('/?lookup=01%2F02%2F03%2F04')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.data, '{"name": "Area"}')


if __name__ == '__main__':
    unittest.main()
