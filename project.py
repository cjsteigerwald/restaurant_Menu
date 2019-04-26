#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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

# Making an API Endpoint (GET Request) for transmitting JSON 
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    # DB.py file must have definition for serialize
    return jsonify(MenuItems=[i.serialize for i in items])


# Display a restaurant menu
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template(
        'menu.html', restaurant=restaurant, items=items)

# Create new restaurant item
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    # Method from newmenuitem.html
    if request.method == 'POST':
        #newItem = MenuItem(name=request.form['name'], description=request.form[
        #        'description'], price=request.form['price'], 
        #        course=request.form['course'], restaurant_id=restaurant_id)
        newItem = MenuItem(name = request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        # send message to User
        flash("%s menu item created!" % newItem.name)
        # redirect user after submitting form, redirecting to restaurantMenu 
        # with variable restaurant_id. This function call must match expected
        # arguments.
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)
        
# Edit restaurant menu
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    # If this is a POST request
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("%s menu item edited!" % editedItem.name)
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        # 3 variables passed into render_template allows editmenuitem.html
        # access to them, the restaurant.id, menuItem.id, and the editedItem
        # object.
        # This is a GET response. With the html template to display, passing in
        # variables used in the template.
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, 
            menu_id = menu_id, item=editedItem)

# Delete item from restaurant menu
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("%s menu item deleted!" % deletedItem.name)
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', 
        restaurant_id = restaurant_id, item = deletedItem)

if __name__ == '__main__':
    # Flask uses to create messages for users
    app.secret_key = 'super_secret_key'
    # Logging to terminal
    app.debug = True
    # listen to port 5000 on all public IP
    app.run(host='0.0.0.0', port=5000)
