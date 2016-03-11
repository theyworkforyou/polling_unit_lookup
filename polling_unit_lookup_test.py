from polling_unit_lookup import app, tidy_up_pun
import unittest
import requests_mock
import json


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

        self.mapit_area = {
            'id': 42,
            'name': 'Aba North',
        }

        self.states = {
            2: {
                'name': 'Abia',
            },
        }

        self.federal_constituencies = {
            1109: {
                'name': 'Aba North/South',
            },
        }

        self.senatorial_districts = {
            811: {
                'name': 'ABIA SOUTH',
            },
        }

    def mock_mapit_response(self, m, pun):
        m.get(
            'http://mapit/code/poll_unit/{}'.format(pun),
            headers={'Location': 'http://mapit/area/42'},
            status_code=302)
        m.get('http://mapit/area/42', json=self.mapit_area)
        m.get('http://mapit/area/42/covered?type=STA', json=self.states)
        m.get('http://mapit/area/42/covered?type=FED', json=self.federal_constituencies)
        m.get('http://mapit/area/42/covered?type=SEN', json=self.senatorial_districts)
        return {
            'area': self.mapit_area,
            'states': [
                self.states[2],
            ],
            'federal_constituencies': [
                self.federal_constituencies[1109],
            ],
            'senatorial_districts': [
                self.senatorial_districts[811],
            ],
        }

    def test_polling_unit_lookup_invalid_number(self):
        rv = self.app.get('/?lookup=abcd')
        self.assertIn('Invalid polling unit: abcd', rv.data)
        self.assertEqual(rv.status_code, 400)

    def test_polling_unit_lookup_valid_number(self):
        with requests_mock.mock() as m:
            expected = self.mock_mapit_response(m, 'AB:1:23:45')
            rv = self.app.get('/?lookup=AB%3A01%3A23%3A45')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(expected, json.loads(rv.data))

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
            expected = self.mock_mapit_response(m, 'AB')
            rv = self.app.get('/?lookup=AB%3A01%3A23%3A45')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(expected, json.loads(rv.data))

    def test_lookup_with_slashes(self):
        with requests_mock.mock() as m:
            expected = self.mock_mapit_response(m, 'AB:2:3:4')
            rv = self.app.get('/?lookup=01%2F02%2F03%2F04')
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(expected, json.loads(rv.data))


if __name__ == '__main__':
    unittest.main()
