#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for
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
    # Old way
    '''
    output = ''
    for i in items:
        output += '<p>'
        output += i.name
        output += '</br> %s' % i.price
        output += '</br> %s' % i.description
        output += '</p>'
    return output
    '''
    # new way of rendering html
    return render_template('menu.html', restaurant=restaurant, items = items)


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    # Method from newmenuitem.html
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], 
        restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        # redirect user after submitting form
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, 
            menu_id = menu_id, item=editedItem)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"




if __name__ == '__main__':
    # Logging to terminal
    app.debug = True
    # listen to port 5000 on all public IP
    app.run(host='0.0.0.0', port=5000)