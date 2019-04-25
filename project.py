#!/usr/bin/env python
from flask import Flask
from flask import request
# Import CRUD Operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)





# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = ''
    for i in items:
        output += '<p>'
        output += i.name
        output += '</br> %s' % i.price
        output += '</br> %s' % i.description
        output += '</p>'
    return output




if __name__ == '__main__':
    # Logging to terminal
    app.debug = True
    # listen to port 5000 on all public IP
    app.run(host='0.0.0.0', port=5000)
