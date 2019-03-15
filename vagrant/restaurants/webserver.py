from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant

# Connect to database
engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind = engine)
session = DBSession()

## Make handler
class webserverHandler(BaseHTTPRequestHandler):
    # I think do_GET is a special function name used by the HTTPServer 
    # function, along with do_POST
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "Hello! <a href=\"/hola\">Link to hola page!</a>"
                output += """<form action='/hello' method='post' enctype='multipart/form-data'>
                <h2> What do you want to say? </h2>
                <input type='text' name='message'>
                <input type='submit' value='Submit'>
                </form>
                """
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>&#161Hola! <a href=\"/hello\">Link to hello page!</a></body></html>"
                output += """<form action='/hola' method='post' enctype='multipart/form-data'>
                <h2> What do you want to say? </h2>
                <input type='text' name='message'>
                <input type='submit' value='Submit'>
                </form>
                """
                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/restaurants'):
                self.send_response(200) # OK response for get request from client
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<!DOCTYPE><html><body>"
                output += '<p><a href="/new">Create a new restaurant</a></p>'
                # Iteratively populate page from database
                for restaurant_name in session.query(Restaurant.name).order_by(Restaurant.id):
                    output += '<p>%s<br>' % restaurant_name
                    output += '<a href=#>Edit</a><br>'
                    output += '<a href=#>Delete</a>'
                    output += '</p>'
                output += '</body></html>'
                self.wfile.write(output)
                return
            if self.path.endswith('/restaurants/new'):
                self.send_response(200) # OK response for get request from client
                self.send_header('Content-type', 'text/html')
                self.end_headers()
        except IOError:
            self.send_error(404, "File Not Found: %s" % self.path)
    
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += "<h2> You said: </h2>"
            output += " %s " % messagecontent[0]
            output += """<form action='/hello' method='post' enctype='multipart/form-data'>
                <h2> What do you want to say? </h2>
                <input type='text' name='message'>
                <input type='submit' value='Submit'>
                </form>
                """
            output += "</body></html>"
            self.wfile.write(output)
            print output
        except:
            pass


## Make main
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()
        
        
if __name__ == '__main__':
    main()