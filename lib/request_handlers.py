"""
All of the RequestHandlers live here. These are akin to traditional Controllers
or Django "views".
"""
import os
import sys
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.db import GeoPt, Key

from oponger_email import send_email
from models import Player, Game
from base_handler import BaseHandler

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
    self.player.pseudonym = self.request.get('pseudonym')
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

