from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from lib.request_handlers import MainPage, NewPlayer, UpdatePlayer, NewGame

application = webapp.WSGIApplication(
  [('/', MainPage),
  ('/player/new', NewPlayer),
  ('/player/update', UpdatePlayer),
  ('/game/new', NewGame)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

