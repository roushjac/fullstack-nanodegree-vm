import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# create instance of special sqlalchemy class -
# python classes interacting with the DB are derived from this class
Base = declarative_base()

### Here, python classes represent tables in a DB

class Restaurant(Base):
	# Table info
	__tablename__ = 'restaurant'
	
	# Mappers
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	

class MenuItem(Base):
	# Table info
	__tablename__ = 'menu_item'
	
	# Mappers
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	# make foreign key relationship with restaurant table
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)



engine = create_engine('sqlite:///restaurantmenu.db')
# add our custom classes as tables into the DB
Base.metadata.create_all(engine)

