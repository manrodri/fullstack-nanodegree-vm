from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

restaurants = session.query(Restaurant).all()
print 'Printing all restaurants'
for restaurant in restaurants:
    print '1.- {}'.format(restaurant.name)
