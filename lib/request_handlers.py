"""
All of the RequestHandlers live here. These are akin to traditional Controllers
or Django "views".
"""
import os
import sys
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.db import GeoPt

from oponger_email import send_email
from locations import LOCATIONS
from models import Player, Game

"""Templates live in this path-relative directory."""
PATH_TO_TEMPLATES = os.path.join(os.path.dirname(__file__),"../templates")

def render_to_response(response, template_name, template_values):
  """Opens the given template and renders the values to the response."""
  path = os.path.join(PATH_TO_TEMPLATES, 'index.html')
  response.out.write(template.render(path, template_values))

class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()

    if user:
      template_values = {
        'nickname'  : user.nickname(),
        'players'   : Player.all(),
        'open_games': Game.gql("WHERE player_2 != NULL and completed_date = NULL"),
        'available_games': Game.gql("WHERE player_2 = NULL"),
        'locations' : LOCATIONS
      }

      player = Player.get_by_key_name(user.user_id()) 
      if player:
        template_values['player'] = player

      render_to_response(self.response, "index.html", template_values)
                              
    else:
      self.redirect(users.create_login_url(self.request.uri))

class NewPlayer(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      
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

class UpdatePlayer(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      
    player = Player.get_by_key_name(user.user_id()) 
    player.pseudonym = self.request.get('pseudonym')
    (lat, lon) = self.request.get('location').split(',')
    player.location = GeoPt(lat, lon)
    player.put()
    self.redirect('/')

class NewGame(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))

    player = Player.get_by_key_name(user.user_id())
    if not player:
      raise "A user must be a player to start a game."

    game = Game(player_1 = player)
    game.put()
    logging.info("Creating new game %s" % (game))
    self.redirect('/')

