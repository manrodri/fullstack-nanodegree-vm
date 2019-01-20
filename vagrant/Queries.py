from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

class Queries:
    def __init__(self, database):
        self.database = database
        engine = create_engine(self.database)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def get_all_items_of_column(self, table, ordered=False):
        if not ordered:
            items = self.session.query(table).all()
        else:
            items = self.session.query(table).order_by('id').all()
        return items

    def print_all_items(self, items):
        for item in items:
            print item.name

def get_all_restaurants():
    q = Queries('sqlite:///restaurantmenu.db')
    restaurants = q.get_all_items_of_column(Restaurant, ordered=True)
    return restaurants

