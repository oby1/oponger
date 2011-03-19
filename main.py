import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from lib.page_handlers import MainPage,\
  UpdateProfile,\
  NewGame,\
  Rulez,\
  Players,\
  Games,\
  PlayerDetails,\
  Profile,\
  JoinGame,\
  CancelGame,\
  CompleteGame

application = webapp.WSGIApplication(
  [('/', MainPage),
  ('/profile', Profile),
  ('/profile/update', UpdateProfile),
  ('/rulez', Rulez),
  ('/players', Players),
  (r'/player/(?P<player_key_name>\w+)', PlayerDetails),
  ('/games', Games),
  ('/game/new', NewGame),
  ('/game/join', JoinGame),
  ('/game/cancel', CancelGame),
  ('/game/complete', CompleteGame)],
  debug=True)

def main():
  logging.getLogger().setLevel(logging.DEBUG)
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

