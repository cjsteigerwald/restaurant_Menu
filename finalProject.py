#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

# Import CRUD Operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake Restaurants
#restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

#restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
#item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

# Homepage that will display restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

# Page for creating a restaurant
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("%s Restaurant Created!" % newRestaurant.name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


# Page for editing a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant_to_Edit = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Edit':
            restaurant_to_Edit.name = request.form['name']
            session.add(restaurant_to_Edit)
            session.commit()
            flash("%s Restaurant Edited!" % restaurant_to_Edit.name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant = restaurant_to_Edit)
	

# Page for deleting a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant_to_delete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Delete':
            session.delete(restaurant_to_delete)
            session.commit()
            flash("%s Restaurant Deleted!" % restaurant_to_delete.name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant = restaurant_to_delete)

# Page for displaying restaurant menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one() 
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)   
    return render_template('menu.html', restaurant = restaurant, items = items) 

# Page to add new menu item for restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(name = request.form['name'], restaurant_id = restaurant_id,
            description = request.form['description'], price = request.form['price'],
            course = request.form['course'])
        session.add(new_item)
        session.commit()
        flash("%s Menu Item Created!" % new_item.name)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id = restaurant_id)

# Page to edit menu item
@app.route('/restaurant/<int:restaurant_id>/<int:items_id>/menu/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, items_id):
    item_to_edit = session.query(MenuItem).filter_by(id=items_id).one()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Edit':
            if request.form['name']:
                item_to_edit.name = request.form['name']
            if request.form['description']:
                item_to_edit.description = request.form['description']
            if request.form['price']:
                item_to_edit.price = request.form['price']
            if 'course' in request.form:
                item_to_edit.course = request.form['course']
            session.add(item_to_edit)
            session.commit()
            flash("%s Menu Item Edited!" % item_to_edit.name)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, item = item_to_edit)

# Page to delete menu item
@app.route('/restaurant/<int:restaurant_id>/<int:items_id>/menu/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, items_id):
    item_to_delete = session.query(MenuItem).filter_by(id=items_id).one()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Delete':
            session.delete(item_to_delete)
            session.commit()               
            flash("%s Menu Item Deleted!" % item_to_delete.name)    
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id,
        item = item_to_delete)

# Making an API Endpoint (GET Request) for sending a list of restaurants JSON 
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()    
    # DB.py file must have definition for serialize
    return jsonify(Restaurants=[i.serialize for i in restaurants])

# Making an API Endpoint (GET Request) for sending a restaurant menu JSON 
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    # DB.py file must have definition for serialize
    return jsonify(MenuItems=[i.serialize for i in items])

# API endpoint (GET Request) for sending a menu item JSON
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem = menuItem.serialize)

if __name__ == '__main__':
    # Flask uses to create messages for users
    app.secret_key = 'super_secret_key'
    # Logging to terminal
    app.debug = True
    # listen to port 5000 on all public IP
    app.run(host='0.0.0.0', port=5000)

