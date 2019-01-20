from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

spanish_restaurant_1 = Restaurant(name='El rinconcillo')
chinesse_restaurant_1 = Restaurant(name='Chinesse Wall')
session.add(chinesse_restaurant_1)
session.add(spanish_restaurant_1)

black_bean_beef = MenuItem(name='Black Beans Beef', course='Entree', description='organic beef in black bean sauce', price='$15.99', restaurant=chinesse_restaurant_1)
spanish_omellet = MenuItem(name='Spanish Omellet', course='Entree', description='Potato and onion omellet made with olive oil and free range eggs', price='$12.99', restaurant=spanish_restaurant_1)

session.commit()
