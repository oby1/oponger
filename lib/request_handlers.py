"""
All of the RequestHandlers live here. These are akin to traditional Controllers
or Django "views".
"""
import os
import sys
import logging
from cgi import escape
from datetime import datetime

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.db import GeoPt, Key

from oponger_email import send_email
from models import Player, Game
from base_handler import BaseHandler
from rules import validate_scores

class MainPage(BaseHandler):
  def DoGet(self):

    additional_values = {
      'open_games': Game.gql("WHERE player_2 != NULL and completed_date = NULL"),
      'available_games': Game.gql("WHERE player_2 = NULL"),
    }
    
    self.template_values.update(additional_values)
    self.render_to_response("index.html")

class Games(BaseHandler):
  def DoGet(self):

    additional_values = {
      'open_games': Game.gql("WHERE player_2 != NULL and completed_date = NULL"),
      'available_games': Game.gql("WHERE player_2 = NULL"),
    }

    self.template_values.update(additional_values)
    self.render_to_response("games.html")

class PlayerDetails(BaseHandler):
  def DoGet(self, player_key_name):
    player_to_show = Player.get_by_key_name(player_key_name)

    logging.info('Getting player %s' % player_to_show)
    if not self.player:
      self.error(404)
      self.response.out.write("""<strong>No player with key %s.
      Try looking through the <a href="/players">list of players</a>.</strong>"""
      % player_key)

    additional_values = {
      'player_to_show'  : player_to_show,
    }

    self.template_values.update(additional_values)
    self.render_to_response("player.html")

class Profile(BaseHandler):
  def DoGet(self):
    self.render_to_response("profile.html")

class Players(BaseHandler):
  def DoGet(self):

    additional_values = {
      'players'   : Player.all(),
    }

    self.template_values.update(additional_values)
    self.render_to_response("players.html")

class Rulez(BaseHandler):
  def DoGet(self):
    self.render_to_response("rulez.html")

class UpdateProfile(BaseHandler):
  def DoPost(self):
    logging.info("Updating player info")
    self.player.pseudonym = escape(self.request.get('pseudonym'))
    (lat, lon) = self.request.get('location').split(',')
    self.player.location = GeoPt(lat, lon)
    self.player.put()
    self.redirect('/profile')

class NewGame(BaseHandler):
  def DoPost(self):
    game = Game(player_1 = self.player)
    game.put()
    logging.info("Creating new game %s" % (game))
    self.redirect('/games')

class JoinGame(BaseHandler):
  def DoPost(self):
    game = Game.get_by_id(long(self.request.get('game_id')))

    if game.player_1 == self.player:
      raise Exception("You can't join your own game, duderino!")
    if game.player_2:
      raise Exception("Oops, looks like someone already joined this game, duderino!")

    game.player_2 = self.player
    game.put()
    logging.info("Player %s joined game %s" % (self.player, game))
    self.redirect('/games')

class CancelGame(BaseHandler):
  def DoPost(self):
    game = Game.get_by_id(long(self.request.get('game_id')))

    if game.player_1.key() != self.player.key():
      raise Exception("You can't delete a game you don't own, duderino!")

    if game.completed_date != None:
      raise Exception("You can't delete a game that's already been completed, duderino!")

    game.delete()
    logging.info("Player %s deleted game %s" % (self.player, game))
    self.redirect('/games')

class CompleteGame(BaseHandler):
  def DoPost(self):
    game = Game.get_by_id(long(self.request.get('game_id')))

    if not (game.player_1.key() == self.player.key() or
        game.player_2.key() == self.player.key()):
      raise Exception("You can't complete a game you don't own, duderino!")

    if game.completed_date != None:
      raise Exception("You can't complete a game that's already been completed, duderino!")
    
    player_1_score = long(self.request.get('player_1_score'))
    player_2_score = long(self.request.get('player_2_score'))
    validate_scores(player_1_score, player_2_score)

    game.completed_date = datetime.now()
    game.player_1_score = player_1_score
    game.player_2_score = player_2_score
    game.put()
    logging.info("Player %s completed game %s" % (self.player, game))
    self.redirect('/games')

