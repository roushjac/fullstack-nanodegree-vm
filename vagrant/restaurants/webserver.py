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
    # object, along with do_POST
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
                output += '<p><a href="/restaurants/new">Create a new restaurant</a></p>'
                # Iteratively populate page from database
                for restaurant in session.query(Restaurant).order_by(Restaurant.id):
                    output += '<p>%s<br>' % restaurant.name
                    output += '<a href=/restaurants/%s/edit>Edit</a><br>' % restaurant.id
                    output += '<a href=/restaurants/%s/delete>Delete</a>' % restaurant.id
                    output += '</p>'
                output += '</body></html>'
                self.wfile.write(output)
                return
            if self.path.endswith('/restaurants/new'):
                self.send_response(200) # OK response for get request from client
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += "<!DOCTYPE><html><body>"
                output += '<h2> Enter a name for a new restaurant </h2>'
                output += '''<form method='post' action ='/restaurants/new' enctype='multipart/form-data'>
                <input type='text' name='new_rest_name'>
                <input type='submit' value='Submit'>
                </form>
                '''
                output += '</body></html>'
                self.wfile.write(output)
                return
                
            if self.path.endswith('/edit'):
                self.send_response(200) # OK response for get request from client
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_id = int(self.path.split('/')[2]) # picks restaurant id from the URL - probably not the best way to do this
                output = '<html><body>'
                output += '<h4>Change name of %s </h4>' % session.query(Restaurant.name).filter_by(id = restaurant_id).first()
                output += '''<form method='post' enctype='multipart/form-data'>
                <input type='text' name='rename'>
                <input type='submit' value='Submit'>
                </form>
                '''
                output += '</body></html>'
                self.wfile.write(output)
                return
            if self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant_id = int(self.path.split('/')[2]) # picks restaurant id from the URL - probably not the best way to do this
                output = '<html><body>'
                output += '<h2> Do you want to delete %s from the website? </h2>' % session.query(Restaurant.name).filter_by(id = restaurant_id).one()
                output += '''
                <form method='post' enctype='multipart/form-data'>
                <input type='submit' value='Delete'>
                </form>
                '''
                output += '</body></html>'
                self.wfile.write(output)
                return
                
                
        except IOError:
            self.send_error(404, "File Not Found: %s" % self.path)
    
    def do_POST(self):
        try:
            if self.path.endswith('/hello') or self.path.endswith('/hola'):
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
                output += """<form method='post' enctype='multipart/form-data'>
                    <h2> What do you want to say? </h2>
                    <input type='text' name='message'>
                    <input type='submit' value='Submit'>
                    </form>
                    """
                output += "</body></html>"
                self.wfile.write(output)
                print output
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_rest_name')
                session.add(Restaurant(name=messagecontent[0]))
                session.commit()
                self.send_response(301)
                self.send_header('Location', '/restaurants')
                self.end_headers()
                
            if self.path.endswith('/edit'):
                restaurant_id = int(self.path.split('/')[2])
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('rename')
                this_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
                this_restaurant.name = messagecontent[0]
                session.commit()
                self.send_response(301) # Successful POST
                self.send_header('Location', '/restaurants')
                self.end_headers()
            if self.path.endswith('/delete'):
                restaurant_id = int(self.path.split('/')[2])
                this_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                session.delete(this_restaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Location', '/restaurants')
                send.end_headers()
                
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