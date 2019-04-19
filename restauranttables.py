from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
# A restaurant object is created 
myFirstRestaurant = Restaurant(name = "Pizza Palace")
# staging myFirstRestaurant object
session.add(myFirstRestaurant)
# commiting myFirstRestaurant object to DB
session.commit()
# run quesry to verify that Restaurant object saved
#session.query(Restaurant).all()
# create menu Item object to the Restaurant DB
cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all "
"natural ingredients and fresh mozzarella", course = "Entree", price = "8.99 ",
restaurant = myFirstRestaurant)
# stage menu item object
session.add(cheesepizza)
# commit to DB
session.commit()

