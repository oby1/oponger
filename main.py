from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from lib.request_handlers import MainPage, UpdatePlayer, NewGame, Rulez, Players, Games, PlayerDetails, Profile

application = webapp.WSGIApplication(
  [('/', MainPage),
  ('/profile', Profile),
  ('/rulez', Rulez),
  ('/players', Players),
  (r'/player/(?P<player_key_name>\w+)', PlayerDetails),
  ('/player/update', UpdatePlayer),
  ('/games', Games),
  ('/game/new', NewGame)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

