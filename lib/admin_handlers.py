import logging
from lib.base_handler import BaseHandler
from lib.models import Player, Game


class MainPage(BaseHandler):
  def DoGet(self):
    self.render_to_response("admin_index.html")

class UpdateSchema(BaseHandler):
  def DoGet(self):
    # By loading and storing each player, we're updating the player for any
    # schema changes.
    # This will not work once we have more than 1000 records, but it's fine for now.
    for player in Player.all():
      player.put()

    for game in Game.all():
      game.put()

    self.render_to_response("update_schema.html")

class UpdateWinnersFromOldSchema(BaseHandler):
  """ Used to migrate the schema from the notion of player scores to a simpler win/lose model"""
  def DoGet(self):

    for game in Game.all():
      logging.info('Checking if game %s is on the new schema' % game)
      if (not game.winner) and hasattr(game, 'player_1_score') and hasattr(game, 'player_2_score'):
        logging.info('Updating Game %s to new schema' % game)
        if game.player_1_score > game.player_2_score:
          game.winner = game.player_1
        else:
          game.winner = game.player_2
        game.put()

    self.render_to_response("update_schema.html")

