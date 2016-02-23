import polling_unit_lookup
import unittest
import requests_mock


class PollingUnitLookupTestCase(unittest.TestCase):

    def setUp(self):
        polling_unit_lookup.app.config['TESTING'] = True
        self.app = polling_unit_lookup.app.test_client()

    def test_polling_unit_lookup_invalid_number(self):
        rv = self.app.get('/?q=abcd')
        assert 'abcd is not a valid polling unit number' in rv.data

    def test_polling_unit_lookup_valid_number(self):
        with requests_mock.mock() as m:
            m.get('http://www.shineyoureye.org/mapit/code/poll_unit/AB:1:23:45',
                  headers={
                      'Location': 'http://www.shineyoureye.org/mapit/area/84'
                  })
            rv = self.app.get('/?q=AB:01:23:45')
            self.assertEqual(rv.headers.get('location'), 'http://www.shineyoureye.org/mapit/area/84')

if __name__ == '__main__':
    unittest.main()
