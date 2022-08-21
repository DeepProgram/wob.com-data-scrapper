from wob.main import get_category_info
from unittest import mock


@mock.patch("wob.main.get_text_response_of_url")
def test_get_category_info_book_valid(mock_response_text, product_info_html):
    output_dict = {'Sku': 'GOR008011677', 'ISBN 13': '9781471156267', 'ISBN 10': '1471156265',
                   'Title': 'It Ends With Us by Colleen Hoover', 'Author': 'Colleen Hoover',
                   'Publisher': 'Simon & Schuster Ltd', 'Year published': '2016-08-02', 'Price': '£8.49'}
    mock_response_text.return_value = product_info_html
    assert get_category_info("https://www.wob.com/en-gb/books/colleen-hoover/it-ends-with-us/9781471156267",
                             True) == output_dict


@mock.patch("wob.main.get_text_response_of_url")
def test_get_category_info_book_invalid_url(mock_response_text):
    mock_response_text.return_value = None
    assert get_category_info("https://www.wob.com/en-gb/books/invalid-url", True) is None


@mock.patch("wob.main.get_text_response_of_url")
@mock.patch("wob.main.get_desired_product_info")
def test_get_category_info_book_invalid_html(mock_desired_product_info, mock_response_text):
    mock_desired_product_info.return_value = None
    mock_response_text.return_value = '<p>Some Invalid Response Data, No Product Info There</p>'
    assert get_category_info("https://www.wob.com/en-gb/books/colleen-hoover/it-ends-with-us/9781471156267",
                             True) is None
