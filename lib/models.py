"""
All of our data models go here.

For details on how Google App Engine handles these, see:
http://code.google.com/appengine/docs/python/datastore/modelclass.html
"""
from google.appengine.ext import db
from locations import DC

MAX_RESULTS=1000

class Player(db.Model):
  date = db.DateTimeProperty(auto_now_add=True)
  user = db.UserProperty(required=True)
  pseudonym = db.StringProperty()
  location = db.GeoPtProperty(default=DC['geoPt'])

  def __str__(self):
    return "[Psuedonym: %s, Nickname: %s]" % (self.pseudonym, self.user.nickname())

  def games(self):
    """Returns this player's games, sorted by creation date."""
    games = self.game_set_1.order("created_date").fetch(MAX_RESULTS, 0)
    games.extend(self.game_set_2.order('created_date').fetch(MAX_RESULTS, 0))
    return sorted(games, key = lambda game: game.created_date, reverse=True)

  def active_games(self):
    return [game for game in self.games() if game.is_active()]

  def available_games(self):
    return [game for game in self.games() if game.is_available()]

  def completed_games(self):
    completed_games = [game for game in self.games() if game.is_completed()]
    return sorted(completed_games, key = lambda game: game.completed_date, reverse=True)

class Game(db.Model):
  created_date = db.DateTimeProperty(auto_now_add=True)
  completed_date = db.DateTimeProperty()
  """The player who created the game."""
  player_1 = db.ReferenceProperty(Player, collection_name='game_set_1')
  """The player who joined the game."""
  player_2 = db.ReferenceProperty(Player, collection_name='game_set_2')
  player_1_score = db.IntegerProperty()
  player_2_score = db.IntegerProperty()

  def __str__(self):
    return "[Player_1: %s, Player_2: %s, Created: %s]" % (self.player_1, self.player_2, self.created_date)

  def is_active(self):
    return self.player_1 != None and self.player_2 != None and self.completed_date == None

  def is_available(self):
    return self.player_1 == None or self.player_2 == None

  def is_completed(self):
    return self.completed_date != None

  def winner(self):
    if self.completed_date == None:
      raise Exception("Can't have a winner for a game which hasn't been completed")
    return self.player_1 if self.player_1_score > self.player_2_score else self.player_2

  @staticmethod
  def all_active():
    return Game.gql("WHERE player_2 != NULL AND completed_date = NULL ORDER BY player_2, created_date DESC")

  @staticmethod
  def all_available():
    return Game.gql("WHERE player_2 = NULL ORDER BY created_date DESC")

  @staticmethod
  def all_completed():
    return Game.gql("WHERE completed_date != NULL ORDER BY completed_date, created_date DESC")

