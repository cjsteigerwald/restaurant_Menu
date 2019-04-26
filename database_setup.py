
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# instance of declarative base class
Base = declarative_base()

# extends BASE
# this represents a table
class Restaurant(Base):
    # representation of our table inside DB
    __tablename__= 'restaurant'

    # creating columns of table
    name = Column(String(80), nullable = False)
    # Primary Key
    id = Column(Integer, primary_key = True)
    # This serialize function allows JSON objects to be sent in a 
    # serializable format
    @property
    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id
        }


# extends BASE
# this represents a table
class MenuItem(Base):
     __tablename__= 'menu_item'

     name = Column(String(80), nullable = False)
     # Primary Key
     id = Column(Integer, primary_key = True)
     course = Column(String(250))
     description = Column(String(250))
     price = Column(String(8))
     # Foreign Key -> restaurant.id
     restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
     # creates relationship with class Restaurant
     restaurant = relationship(Restaurant)

     @property
     def serialize(self):
         return {
             'id' : self.id,
             'course' : self.course,
             'description' : self.description,
             'restaurant_id' : self.restaurant_id
         }

# create instance of create database class
# and point to db to use
### insert at end of file ###
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
