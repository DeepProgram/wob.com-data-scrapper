from unittest import mock

import pytest
from bs4 import BeautifulSoup

from wob.main import get_text_response_of_url, search_book_info_list, search_for_other_than_book, find_element_in_soup, \
    process_info, get_book_info_template, get_template_other_than_book, get_price_element, get_price_text, \
    get_valid_product_attribute_and_value, get_desired_product_info


def string_to_bs4_element(string):
    return BeautifulSoup(string, "html.parser")


def test_search_book_info_list():
    assert search_book_info_list() == ["Sku", "ISBN 13", "ISBN 10", "Title", "Author", "Publisher", "Year published"]


def test_search_for_other_than_book():
    assert search_for_other_than_book() == ["Sku", "Title", "Studio", "EAN", "Release date"]


@pytest.mark.parametrize("url, output", [("https://wob.com", "Some HTML File")])
@mock.patch("wob.main.requests.get")
def test_requests_get_valid(mock_requests_get, url, output):
    mock_requests_get.return_value = mock.Mock(name="Requests Response", **{"text": output})
    assert get_text_response_of_url(url) == "Some HTML File"


@pytest.mark.parametrize("url, output", [("https://", None)])
@mock.patch("wob.main.requests.get")
def test_requests_get_invalid(mock_requests_get, url, output):
    mock_requests_get.side_effect = Exception("Couldn't Connect To Website.. Try Again.... ")
    assert get_text_response_of_url(url) is None


@pytest.fixture(scope="module")
def search_element_from_html_main_page():
    with open("files_for_testing/desired_html_elements_main_page.txt", "r") as file:
        return file.read()[:-1]


def test_find_element_in_soup_main_page_valid_find_all(search_element_from_html_main_page):
    with open("files_for_testing/html_main_page.txt", "r") as file:
        string_data = str(
            find_element_in_soup(file.read(), "div", {'class': 'categoryItem'},
                                 True)).encode("utf-8").decode()
        assert string_data == search_element_from_html_main_page


def test_find_element_in_soup_main_page_valid_find(product_info_html, search_element_from_html_main_page):
    assert str(find_element_in_soup(product_info_html, "div", {"class": "price"},
                                    False)) == '<div class="price">£8.49</div>'


def test_find_element_in_soup_main_page_invalid_find_all():
    html_string = "<span> This Is Not The Desired Element</span>"
    assert find_element_in_soup(html_string, "div", {'class': 'categoryItem'}, True) is None


def test_find_element_in_soup_main_page_invalid_find():
    html_string = "<span> This Is Not The Desired Element</span>"
    assert find_element_in_soup(html_string, "div", {'class': 'categoryItem'}, False) is None


def test_find_element_in_soup_not_enough_pages():
    with open("files_for_testing/page_not_found_html.txt", "r") as file:
        assert find_element_in_soup(file.read(), "h1", {"class": "title"}, False) == "Not Enough Pages"


@pytest.mark.parametrize("label,div,is_book, output", [
    ('Sku', 'GOR007760197', True, ['Sku', 'GOR007760197']),
    ('ISBN 13', '9781471156267', True, ['ISBN 13', '9781471156267']),
    ('ISBN 10', '1471156265', True, ['ISBN 10', '1471156265']),
    ('Title', 'It Ends With Us by Colleen Hoover', True, ['Title', 'It Ends With Us by Colleen Hoover']),
    ('Author', 'Colleen Hoover', True, ['Author', 'Colleen Hoover']),
    ('Condition', 'Used - Very Good', True, None),
    ('Binding type', 'Paperback', True, None),
    ('Publisher', 'Simon & Schuster Ltd', True, ['Publisher', 'Simon & Schuster Ltd']),
    ('Year published', '2016-08-02', True, ['Year published', '2016-08-02']),
    ('Number of pages', '384', True, None),
    ('Prizes', 'N/A', True, None),
    ('Cover note', 'Book picture is for illustrative purposes only, actual binding, cover or edition may vary.',
     True, None),
    ('Note', 'This is a used book - there is no escaping the fact it has been read by someone else and it will '
             'show signs of wear and previous use. Overall we expect it to be in very good condition, but if '
             'you are not entirely satisfied please get in touch with us',
     True, None),
    ('Number of pages', '384', True, None)
])
def test_process_info(label, div, is_book, output):
    assert process_info(label, div, is_book) == output


def test_get_book_info_template():
    assert get_book_info_template() == {
        "Sku": "",
        "ISBN 13": "",
        "ISBN 10": "",
        "Title": "",
        "Author": "",
        "Publisher": "",
        "Year published": "",
        "Price": ""
    }


def test_get_template_other_than_book():
    assert get_template_other_than_book() == {
        "Sku": "",
        "Title": "",
        "Studio": "",
        "EAN": "",
        "Release date": "",
        "Price": ""
    }


def test_get_price_element_valid(product_info_html):
    assert str(get_price_element(product_info_html)) == '<div class="price">£8.49</div>'


def test_get_price_element_invalid():
    assert get_price_element('<p>Some Invalid Product Elements</p>') is None


def test_get_price_text_valid(product_info_html):
    assert get_price_text(product_info_html) == "£8.49"


def test_get_price_text_invalid():
    assert get_price_text('<p>Some Invalid Product Elements</p>') == ""


def test_get_valid_product_attribute_and_value_valid():
    product_attribute = BeautifulSoup('<div class="attribute"><label class="attributeTitle">'
                                      'Sku</label><div class="attributeValue">GOR007760197</div></div>', "html.parser")
    assert get_valid_product_attribute_and_value(product_attribute) == ['Sku', 'SkuGOR007760197']


def test_get_valid_product_attribute_and_value_invalid():
    assert get_valid_product_attribute_and_value(string_to_bs4_element("<p>Some Invalid Product Elements</p>")) == []


def test_get_desired_product_info_valid(product_info_html, product_info_template):
    output_dict = {'Sku': 'GOR008011677', 'ISBN 13': '9781471156267', 'ISBN 10': '1471156265',
                   'Title': 'It Ends With Us by Colleen Hoover', 'Author': 'Colleen Hoover',
                   'Publisher': 'Simon & Schuster Ltd', 'Year published': '2016-08-02', 'Price': '£8.49'}
    assert get_desired_product_info(product_info_html, True, product_info_template) == output_dict


def test_get_desired_product_info_invalid_html(product_info_template):
    invalid_product_html_string = '<p>Invalid Product Info HTML</p>'
    assert get_desired_product_info(invalid_product_html_string, True, product_info_template) is None


def test_get_desired_product_info_invalid_dict(product_info_html):
    invalid_dict = {"dict": "invalid"}
    output_dict = {'dict': 'invalid', 'Sku': 'GOR008011677', 'ISBN 13': '9781471156267', 'ISBN 10': '1471156265',
                   'Title': 'It Ends With Us by Colleen Hoover', 'Author': 'Colleen Hoover',
                   'Publisher': 'Simon & Schuster Ltd', 'Year published': '2016-08-02'}
    assert get_desired_product_info(product_info_html, True, invalid_dict) == output_dict
