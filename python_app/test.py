import unittest
from main import app

# class which contains unit tests
class MyUnitTests(unittest.TestCase):

    def setUp(self):
        # opens up fake browser
        self.client = app.test_client()

    def test_endpoint_code(self):
        # sends http request to / and save the response in a variable
        response = self.client.get('/')

        # check whether the status code is 200
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint_code(self):
        # sends http request to /health and save the response in a variable
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')

if __name__ == '__main__':
    unittest.main()
