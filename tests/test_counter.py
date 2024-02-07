"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        # 1) Make a call to Create a counter.
        result = self.client.post('/counters/woo')
        # 2) Ensure that it returned a successful return code.
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # 3) Check the counter value as a baseline.
        baseline = result.get_json()['woo']
        self.assertEqual(baseline, 0)

        increment = 1

        # 4) Make a call to Update the counter that you just created.
        result = self.client.put('/counters/woo', json=increment)
        # 5) Ensure that it returned a successful return code.
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        updatedValue = result.get_json()['woo']
        # 6) Check that the counter value is one more than the baseline
        self.assertEqual(updatedValue, baseline + increment)

    def test_update_a_nonexistent_counter(self):
        """It should return an error for non-existent counter"""
        result = self.client.post('/counters/doo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        result = self.client.put('/counters/fake')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_a_counter(self):
        """It should get a counter"""
        # Create new counter
        result = self.client.post('/counters/far')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        expectedValue = 0

        # Check counter is 0
        result = self.client.get('/counters/far')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get_json()['far'], expectedValue)

        # Update counter by 1
        result = self.client.put('/counters/far', json=1)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get_json()['far'], expectedValue + 1)

        # Check counter is 1 after update
        result = self.client.get('/counters/far')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get_json()['far'], expectedValue + 1)

    def test_get_a_nonexistent_counter(self):
        """It should return an error for non-existent counter"""
        result = self.client.post('/counters/coo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        result = self.client.get('/counters/fake')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
