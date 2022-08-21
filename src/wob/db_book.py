from typing import Any

from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///sqlalchemy.sqlite.books_info", echo=True)
base: Any = declarative_base()


class Transactions(base):
    __tablename__ = "books_info"
    Category = Column(String)
    Sku = Column(String, primary_key=True)
    ISBN_13 = Column(String)
    ISBN_10 = Column(String)
    Title = Column(String)
    Author = Column(String)
    Publisher = Column(String)
    Year_Published = Column(String)
    Price = Column(String)

    def __init__(self, Category, Sku, ISBN_13, ISBN_10, Title, Author, Publisher, Year_Published, Price):
        self.Category = Category
        self.Sku = Sku
        self.ISBN_13 = ISBN_13
        self.ISBN_10 = ISBN_10
        self.Title = Title
        self.Author = Author
        self.Publisher = Publisher
        self.Year_Published = Year_Published
        self.Price = Price


base.metadata.create_all(engine)
