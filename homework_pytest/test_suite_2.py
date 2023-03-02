import requests
import pytest
from save_data import save_data

url = 'https://docs.pytest.org/en/7.2.x'


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
        response = requests.get(url)

        assert response.status_code == 200

    def test_second(self):
        response = requests.get(f"{url}/getting-started.html")

        assert response.status_code == 200

    def test_third(self, request):
        response = requests.get(f"{url}/test/")
        code = response.status_code
        assert code == 404
