# webserver.py
# Simple HTTP server
from BaseHTTPServer  import BaseHTTPRequestHandler, HTTPServer
import cgi
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
            output += "Hello!"            
            output += "<h1>What would you like me to say?</h1>"
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
            output += "<input name='message' type='text' >"
            output += "<input type='submit' value='Submit'></form>"
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
            output += "</body></html>"
            self.wfile.write(output)
            print(output)
            return
      except IOError:
          self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
      try:
        self.send_response(301)
        self.end_headers()

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if (ctype == 'multipart/form-data'):
          fields = cgi.parse_multipart(self.rfile, pdict)
          messagecontent = fields.get('message')

        output = ""
        output += "<html><body>"
        output +=" <h2>Okay, how about this: </h2>"
        output += "<h1> %s </h1>" % messagecontent[0]

        output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
        output += "<input name='message' type='text' >"
        output += "<input type='submit' value='Submit'></form>"
        output += "</body></html>"
        output += "</body></h"
        self.wfile.write(output)
        print(output)

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
