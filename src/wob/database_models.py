from sqlalchemy import Column, String

from database import Base


class BookInfo(Base):
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


class OtherInfo(Base):
    __tablename__ = "other_info"
    Category = Column(String)
    Sku = Column(String, primary_key=True)
    Title = Column(String)
    Studio = Column(String)
    EAN = Column(String)
    Release_Date = Column(String)
    Price = Column(String)

    def __init__(self, Category, Sku, Title, Studio, EAN, Release_Date, Price):
        self.Category = Category
        self.Sku = Sku
        self.Title = Title
        self.Studio = Studio
        self.EAN = EAN
        self.Release_Date = Release_Date
        self.Price = Price
