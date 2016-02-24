from polling_unit_lookup import app, tidy_up_pun
import unittest
import requests_mock


class TidyUpPunTestCase(unittest.TestCase):
    def test_none_returns_empty_string(self):
        self.assertEqual('', tidy_up_pun(None))

    def test_tidy_up_and_clean(self):
        self.assertEqual('AB:1:23:45', tidy_up_pun('AB:01:23:45'))
        self.assertEqual('AB:1:23:45', tidy_up_pun('AB--01::23 45'))
        self.assertEqual('AB:1:23:45', tidy_up_pun('  AB--01::23 45  '))

    def test_converting_state_number_to_code(self):
        self.assertEqual('AB:1:23:45', tidy_up_pun('01:01:23:45'))
        self.assertEqual('AB', tidy_up_pun('01'))
        self.assertEqual('99:1:23:45', tidy_up_pun('99:01:23:45'))


class PollingUnitLookupTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['MAPIT_API_URL'] = 'http://mapit'
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        self.app = app.test_client()

    def test_polling_unit_lookup_invalid_number(self):
        rv = self.app.get('/?lookup=abcd')
        self.assertIn('Unrecognized polling unit: abcd', rv.data)
        self.assertEqual(rv.status_code, 404)

    def test_polling_unit_lookup_valid_number(self):
        with requests_mock.mock() as m:
            m.get('http://mapit/code/poll_unit/AB:1:23:45', text='{"name": "Area"}')
            rv = self.app.get('/?lookup=AB%3A01%3A23%3A45')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.data, '{"name": "Area"}')

    def test_polling_unit_lookup_valid_number_no_area(self):
        with requests_mock.mock() as m:
            m.get('http://mapit/code/poll_unit/ZZ', status_code=404)
            rv = self.app.get('/?lookup=ZZ')
            self.assertEqual(rv.status_code, 404)
            self.assertIn('No areas were found that matched polling unit: ZZ', rv.data)

    def test_lookup_tries_multiple_variations(self):
        with requests_mock.mock() as m:
            m.get('http://mapit/code/poll_unit/AB:1:23:45', status_code=404)
            m.get('http://mapit/code/poll_unit/AB:1:23', status_code=404)
            m.get('http://mapit/code/poll_unit/AB:1', status_code=404)
            m.get('http://mapit/code/poll_unit/AB', text='{"name": "Area"}')
            rv = self.app.get('/?lookup=AB%3A01%3A23%3A45')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.data, '{"name": "Area"}')

    def test_lookup_with_slashes(self):
        with requests_mock.mock() as m:
            m.get('http://mapit/code/poll_unit/AB:2:3:4', text='{"name": "Area"}')
            rv = self.app.get('/?lookup=01%2F02%2F03%2F04')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.data, '{"name": "Area"}')


if __name__ == '__main__':
    unittest.main()
