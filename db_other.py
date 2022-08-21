from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///sqlalchemy.sqlite.other_info", echo=True)
base = declarative_base()


class Transactions(base):
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


base.metadata.create_all(engine)
