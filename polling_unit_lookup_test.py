import polling_unit_lookup
import unittest

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        polling_unit_lookup.app.config['TESTING'] = True
        self.app = polling_unit_lookup.app.test_client()

    def test_homepage(self):
        rv = self.app.get('/')
        assert 'Hello World!' in rv.data

if __name__ == '__main__':
    unittest.main()
