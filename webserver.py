# webserver.py
# Simple HTTP server
import os
import sys

# Import CRUD Operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from BaseHTTPServer  import BaseHTTPRequestHandler, HTTPServer
import cgi

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Handler class indicates what code to execute based on the type
# of request is sent to the server
class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
      try:  
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Hello!</h1>" 
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
            <h2>What would you like me to say?</h2><input name="message" type="text" >
            <input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print(output)
            return

        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "Hello!"            
            output += "<h1>What would you like me to say?</h1>"
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
            output += "<input name='message' type='text' >"
            output += "<input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output)
            print(output)
            return

        if self.path.endswith("/restaurants"):
            restaurants = session.query(Restaurant).all()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()            
            output = ""
            output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
            output += "<html><body>"
            for restaurant in restaurants:
              output += "<p>"
              output += restaurant.name
              output += "</br>"
              output += "<a href='https://www.w3schools.com/html/'>edit</a>"
              output += "</br>"
              output += "<a href='https://www.w3schools.com/html/'>delete</a>"
              output += "</p>"    
            
            output += "</body></html>"
            self.wfile.write(output)
            print(output)
            return

        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()            
            output = ""
            output += "<html><body>"
            output += "<h1>Make a new Restaurant</h1>"
            output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/new'>"
            output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name'>"
            output += "<input type = 'submit' value = 'Create'>"
            output += "</form></body></html>"
            self.wfile.write(output)
            print(output)
            return
        
      except IOError:
          self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
      try:
        
        if self.path.endswith("/restaurants/new"):
          ctype, pdict = cgi.parse_header(
            self.headers.getheader('content-type')
          )
          if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('newRestaurantName')

            # Create new Restaurant object
            newRestaurant = Restaurant(name=messagecontent[0])
            session.add(newRestaurant)
            session.commit()

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()
        '''
        ctype, pdict = cgi.parse_header(
            self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('message')
        output = ""
        output += "<html><body>"
        output += " <h2> Okay, how about this: </h2>"
        output += "<h1> %s </h1>" % messagecontent[0]
        output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
        output += "<h2>What would you like me to say?</h2>"
        output += "<input name="message" type="text" >"
        output += "<input type="submit" value="Submit"> </form>"
        output += "</body></html>"
        
        self.wfile.write(output)
        print(output)
        '''

      except:
        pass
      

# Instantiate server and specify port it will run on
def main():
  try:
    port = 8080
    server = HTTPServer(('', port), WebServerHandler)
    print("Web Server running on port %s" % port)
    server.serve_forever()
  except KeyboardInterrupt:
    print("^C entered, stopping web server....")
    server.socket.close()

if __name__ == '__main__':
  main()
