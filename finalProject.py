#!/usr/bin/env python

from flask import Flask
app = Flask(__name__)

# Homepage that will display restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return "Show all restaurants"

# Page for creating a restaurant
@app.route('/restaurant/restaurant_id/new/')
def newRestaurant():
    return "This page creates a restaurants"

# Page for editing a restaurant
@app.route('/restaurant/restaurant_id/edit/')
def editRestaurant():
    return "Page to edit restaurant"

# Page for deleting a restaurant
@app.route('/restaurant/restaurant_id/delete/')
def deleteRestaurant():
    return "Page to delete restaurant"


if __name__ == '__main__':
    # Flask uses to create messages for users
    app.secret_key = 'super_secret_key'
    # Logging to terminal
    app.debug = True
    # listen to port 5000 on all public IP
    app.run(host='0.0.0.0', port=5000)

