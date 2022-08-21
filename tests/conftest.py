import pytest
from bs4 import BeautifulSoup


@pytest.fixture(scope="module")
def product_info_html():
    with open("files_for_testing/product_info_html.txt") as file:
        return file.read()


@pytest.fixture
def string_to_bs4_element():
    def _method(string):
        return BeautifulSoup(string, "html.parser")

    return _method


@pytest.fixture
def product_info_template():
    return {'Sku': '', 'ISBN 13': '', 'ISBN 10': '', 'Title': '', 'Author': '', 'Publisher': '',
            'Year published': '', 'Price': '£8.49'}
