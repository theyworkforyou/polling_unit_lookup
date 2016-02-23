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
        rv = self.app.get('/?q=abcd')
        assert 'Unrecognized poll_unit: abcd' in rv.data
        self.assertEqual(rv.status_code, 404)

    def test_polling_unit_lookup_valid_number(self):
        with requests_mock.mock() as m:
            m.get('http://pmo/code/poll_unit/AB:1:23:45', text='{"name": "Area"}')
            rv = self.app.get('/?q=AB:01:23:45')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.data, '{"name": "Area"}')

if __name__ == '__main__':
    unittest.main()
