import polling_unit_lookup
import unittest


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        polling_unit_lookup.app.config['TESTING'] = True
        self.app = polling_unit_lookup.app.test_client()

    def test_polling_unit_lookup(self):
        rv = self.app.get('/?q=abcd')
        assert 'ABCD is not a valid polling unit number' in rv.data
        rv = self.app.get('/?q=AB:01:23:45')
        print(rv.data)
        assert 'AB:1:23:45 is a valid polling unit number' in rv.data

if __name__ == '__main__':
    unittest.main()
