#!/usr/bin/env python

from flask import Flask, render_template
app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

# Homepage that will display restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return render_template('restaurants.html', restaurants = restaurants)

# Page for creating a restaurant
@app.route('/restaurant/restaurant_id/new/')
def newRestaurant():
    return render_template('newRestaurant.html', restaurant = restaurant)

# Page for editing a restaurant
@app.route('/restaurant/restaurant_id/edit/')
def editRestaurant():
    return render_template('editRestaurant.html', restaurant = restaurant)

# Page for deleting a restaurant
@app.route('/restaurant/restaurant_id/delete/')
def deleteRestaurant():
    return render_template('deleteRestaurant.html', restaurant = restaurant)

# Page for displaying restaurant menu
@app.route('/restaurant/restaurant_id/')
@app.route('/restaurant/restaurant_id/menu')
def showMenu():
    return render_template('menu.html', restaurant = restaurant, items = items) 

# Page to add new menu item for restaurant
@app.route('/restaurant/restaurant_id/menu/new/')
def newMenuItem(restaurant_id):
    return render_template('newMenuItem.html', restaurant_id = restaurant_id)

# Page to edit menu item
@app.route('/restaurant/restaurant_id/menu/edit/')
def editMenuItem(restaurant_id, menu_id):
    return render_template('editMenuItem.html', restaurant_id = restaurant_id,
        menu_id = menu_id)

# Page to delete menu item
@app.route('/restaurant/restaurant_id/menu/delete/')
def delteMenuItem(restaurant_id, menu_id):
    deletedItem = menu_id
    return render_template('deleteMenuItem.html', restaurant_id = restaurant_id,
        item = deletedItem)


if __name__ == '__main__':
    # Flask uses to create messages for users
    app.secret_key = 'super_secret_key'
    # Logging to terminal
    app.debug = True
    # listen to port 5000 on all public IP
    app.run(host='0.0.0.0', port=5000)

