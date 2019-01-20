
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi
from Queries import get_all_restaurants



#  create a connection to the db
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith('/delete'):
                restaurantIDPath = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you would like to delete {}</h1>".format(myRestaurantQuery.name)
                    output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/{}/delete'>".format(restaurantIDPath)
                    output += "<input type='submit' value='Delete Restaurant'>"
                    output += "</form></body></html>"
                    self.wfile.write(output)
                    return



            if self.path.endswith('/edit'):
                restaurantIDPath = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>{}</h1>".format(myRestaurantQuery.name)
                    output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/{}/edit'>".format(restaurantIDPath)
                    output += "<input name = 'newRestaurantName' type = 'text' placeholder = '{}' > "\
                        .format(myRestaurantQuery.name)
                    output += "<input type='submit' value='Rename Restaurant'>"
                    output += "</form></body></html>"
                    self.wfile.write(output)
                    return

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>List of susbcribed restaurants</h1>"
                restaurants = get_all_restaurants()
                for restaurant in restaurants:
                    output += '{}'.format(restaurant.name)
                    output += '</br>'
                    # <a href="url">link text</a
                    output += '<a href="/restaurants/{}/edit"> edit</a></br>'.format(str(restaurant.id))
                    output+= '<a href="restaurants/{}/delete"> delete</a></br>'.format(str(restaurant.id))
                    output += "</br>"
                output += "<a href='/restaurants/new'>Make a new restaurant</a>"
                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split('/')[2]

                # delete  Restaurant Object
                myQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myQuery != []:
                    session.delete(myQuery)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split('/')[2]
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # update  Restaurant Object
                    newRestaurant = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    if newRestaurant != []:
                        newRestaurant.name = messagecontent[0]
                        session.add(newRestaurant)
                        session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()


if __name__ == '__main__':
    main()
