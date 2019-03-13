from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# engine is what allows interaction with the DB
engine = create_engine('sqlite:///restaurantmenu.db')
# make all classes use the same metadata, which comes from the DB
# - connects class definitions to the corresponding tables
Base.metadata.bind = engine

# Connection between our code and the engine
DBSession = sessionmaker(bind = engine)
# Changes to the session don't do anything until committed
session = DBSession()

# Add a restaurant into the Restaurant tables
myFirstRestaurant = Restaurant(name = 'The Pizza Place')
session.add(myFirstRestaurant)

# Add MenuItem into the MenuItem table 
cheesePizza = MenuItem(name = "Cheese Pizza",
	description = "All natural ingredients and fresh mozerella",
	course = "Entree", price = "$7.99", 
	restaurant = myFirstRestaurant)
session.add(cheesePizza)

session.commit()