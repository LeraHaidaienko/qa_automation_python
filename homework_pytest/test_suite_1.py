import requests
import pytest


class TestSuite:

    def setup_class(self):
        print('Test Suite started')

    def teardown_class(self):
        print('Test Suite done')

    def setup(self):
        print('single test started')

    def teardonw(self):
        print('single test finished')

    def test_first(self):
        response = requests.get('https://ithillel.ua/')

        assert response.status_code == 200

    def test_second(self):
        response = requests.get('https://ithillel.ua/test')

        assert response.status_code == 404

    def test_third(self):
        response = requests.get('https://odessa.ithillel.ua/')

        assert response.status_code == 200
