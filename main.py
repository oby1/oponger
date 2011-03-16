from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from lib.request_handlers import MainPage, SignUp, UpdatePlayer

application = webapp.WSGIApplication(
  [('/', MainPage),
  ('/signup', SignUp),
  ('/update_player', UpdatePlayer)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

