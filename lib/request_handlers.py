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
from locations import LOCATIONS
from models import Player, Game
from base_handler import BaseHandler

class MainPage(BaseHandler):
  def DoGet(self):

    additional_values = {
      'open_games': Game.gql("WHERE player_2 != NULL and completed_date = NULL"),
      'available_games': Game.gql("WHERE player_2 = NULL"),
      'locations' : LOCATIONS
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
      'is_current_user' : self.player == player_to_show,
      'locations'       : LOCATIONS
    }
    self.template_values.update(additional_values)
    self.render_to_response("player.html")

class Players(BaseHandler):
  def DoGet(self):

    additional_values = {
      'players'   : Player.all(),
      'locations' : LOCATIONS
    }

    self.template_values.update(additional_values)
    self.render_to_response("players.html")

class Rulez(BaseHandler):
  def DoGet(self):
    self.render_to_response("rulez.html")

class NewPlayer(BaseHandler):
  def DoPost(self):
    player = Player.get_or_insert(user.user_id(), user = user, pseudonym = self.request.get('pseudonym'))
    send_email(user,
        """| . |  Welcome to OPONGER, %s! :)""" % (player.pseudonym),
        """Visit http://oponger.opower.com to check out the competition,
        start your first game, or change your details. Happy ponging! :)\n
        |\n
             .\n
        \n
                     |
        """)
    self.redirect('/')

class UpdatePlayer(BaseHandler):
  def DoPost(self):
    player.pseudonym = self.request.get('pseudonym')
    (lat, lon) = self.request.get('location').split(',')
    player.location = GeoPt(lat, lon)
    player.put()
    self.redirect('/')

class NewGame(BaseHandler):
  def DoPost(self):
    if not self.player:
      # TODO: replace with an http error
      raise "A user must be a player to start a game."

    game = Game(player_1 = player)
    game.put()
    logging.info("Creating new game %s" % (game))
    self.redirect('/')
