import pytest


@pytest.fixture(scope="module")
def product_info_html():
    with open("files_for_testing/product_info_html.txt") as file:
        return file.read()


@pytest.fixture
def product_info_template():
    return {'Sku': '', 'ISBN 13': '', 'ISBN 10': '', 'Title': '', 'Author': '', 'Publisher': '',
            'Year published': '', 'Price': '£8.49'}
