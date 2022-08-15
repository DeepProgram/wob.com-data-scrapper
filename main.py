from typing import Optional
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
import db_book
import db_other


def search_book_info_list() -> list:
    return ["Sku", "ISBN 13", "ISBN 10", "Title", "Author", "Publisher", "Year published"]


def search_for_other_than_book() -> list:
    return ["Sku", "Title", "Studio", "EAN", "Release date"]


def get_response_of_url(url: str) -> Optional[str]:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/89.0.4389.90 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print("Couldn't Connect To Website.. Try Again.... ", e)
        return None
    return response.text


def find_element_in_soup(html_string: str, search_element: str, attributes: dict,
                         find_all: bool) -> BeautifulSoup.text:
    try:
        soup = BeautifulSoup(html_string, "html.parser")
        page_title = soup.find("h1", attrs={"class": "title"})
        if page_title is not None and page_title.text == "Page not found":
            return "Not Enough Pages"
        if find_all:
            searched_element = soup.find_all(search_element, attributes)
        else:
            searched_element = soup.find(search_element, attributes)
    except Exception as e:
        print("Couldn't Search The Desired Element.... ", e)
        return None
    return searched_element


def process_info(info_attribute: str, info_value: str, is_book: bool) -> Optional[list]:
    if is_book:
        search_list = search_book_info_list()
        date_attribute = "Year published"
    else:
        search_list = search_for_other_than_book()
        date_attribute = "Release date"
    if info_attribute in search_list:
        if info_attribute == date_attribute and len(info_value) != 4 and "-" not in info_value:
            info_value = info_value[:4] + "-" + info_value[4:6] + "-" + info_value[6:]
        return [info_attribute, info_value]
    else:
        return None


def get_book_info_template() -> dict:
    book_info_dictionary = {
        "Sku": "",
        "ISBN 13": "",
        "ISBN 10": "",
        "Title": "",
        "Author": "",
        "Publisher": "",
        "Year published": "",
        "Price": ""
    }
    return book_info_dictionary


def get_template_other_than_book() -> dict:
    other_info_dictionary = {
        "Sku": "",
        "Title": "",
        "Studio": "",
        "EAN": "",
        "Release date": "",
        "Price": ""
    }
    return other_info_dictionary


def get_category_info(url: str, is_book: bool) -> Optional[dict]:
    if is_book:
        info_dictionary = get_book_info_template()
    else:
        info_dictionary = get_template_other_than_book()
    html = get_response_of_url(url)
    if html is not None:
        price_element = find_element_in_soup(html, "div", {"class": "price"}, False)
        if price_element is not None:
            info_dictionary["Price"] = price_element.text
        info_elements = find_element_in_soup(html, "div", {"class": "attributes"}, False)
        if info_elements is not None:
            for info in info_elements:
                try:
                    label_text = info.label.text
                    div_text = info.div.text
                except AttributeError:
                    continue
                except Exception as e:
                    print(e)
                    continue
                processed_info = process_info(label_text, div_text, is_book)
                if processed_info is not None:
                    info_dictionary[processed_info[0]] = processed_info[1]
        else:
            return None
    return info_dictionary


def process_different_category(session_book, database_book: db_book,
                               session_other, database_other: db_other, search_pages):
    html = get_response_of_url("https://www.wob.com/en-gb")
    if html is not None:
        category_list = find_element_in_soup(html, "div", {"class": "categoryItem"}, True)
        if category_list is not None:
            for category in category_list:
                if category.a is not None:
                    is_book = True if "Books" in category.a.text else False
                    if is_book:
                        process_category(session_book, database_book, "https://www.wob.com" + category.a["href"],
                                         category.a.text, is_book, search_pages)
                    else:
                        process_category(session_other, database_other, "https://www.wob.com" + category.a["href"],
                                         category.a.text, is_book, search_pages)


def process_category(session, db, url: str, category_name: str, is_book: bool, maximum_page_number):
    for page_number in range(1, maximum_page_number+1):
        print("\n\tFetching From : "+url + "/" + str(page_number))
        html = get_response_of_url(url + "/" + str(page_number))
        if html is not None:
            section_list = find_element_in_soup(html, "section", {"class": "productList"}, False)
            if section_list == "Not Enough Pages":
                break
            if section_list is not None:
                for product in section_list.div:
                    product_link = "https://www.wob.com" + product.a["href"]
                    info = get_category_info(product_link, is_book)
                    if info is not None:
                        if not is_already_exist_in_database(session, db, info["Sku"]):
                            if is_book:
                                save_book_in_database(session, db, category_name, info)
                            else:
                                save_others_in_database(session, db, category_name, info)
    session.commit()


def is_already_exist_in_database(session, db, sku: str) -> bool:
    return session.query(exists().where(db.Transactions.Sku == sku)).scalar()


def save_book_in_database(session, db, category_name: str, book_info: dict):
    table_row = db.Transactions(category_name, book_info["Sku"], book_info["ISBN 13"], book_info["ISBN 10"],
                                book_info["Title"],
                                book_info["Author"], book_info["Publisher"], book_info["Year published"],
                                book_info["Price"])

    session.add(table_row)


def save_others_in_database(session, db, category_name: str, other_info: dict):
    table_row = db.Transactions(category_name, other_info["Sku"], other_info["Title"], other_info["Studio"],
                                other_info["EAN"], other_info["Release date"], other_info["Price"])

    session.add(table_row)


def main():
    print("\n\tEnter The Number Of Pages You Want to Search : ", end="")
    try:
        search_number_of_pages = int(input(""))
    except ValueError:
        print("Please Enter Valid INTEGER Number....")
        return
    Session_Book = sessionmaker(bind=db_book.engine)
    session_book_obj = Session_Book()
    Session_Other = sessionmaker(bind=db_other.engine)
    session_other_obj = Session_Other()
    process_different_category(session_book_obj, db_book, session_other_obj, db_other, search_number_of_pages)


if __name__ == '__main__':
    main()
