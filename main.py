import webapp2
from controllers import controllerhandle,crons
from views import viewhandle


print "This is AngelApi app";
application = webapp2.WSGIApplication([
    ('/', controllerhandle.MainHandler),
    ('/post', viewhandle.MainHandler),
    ('/crons', crons.UpdateDatastore)
], debug=True)
