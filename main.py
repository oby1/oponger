from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.db import GeoPt
import os
import sys
from google.appengine.ext.webapp import template
from models import Player
from locations import LOCATIONS

class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    players = db.GqlQuery("SELECT * FROM Player ORDER BY date DESC")

    if user:
      template_values = {
        'nickname'  : user.nickname(),
        'players'   : players,
        'locations' : LOCATIONS
      }

      player = Player.get_by_key_name(user.user_id()) 
      if player:
        template_values['player'] = player

      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))
                              
    else:
      self.redirect(users.create_login_url(self.request.uri))

class SignUp(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      
    player = Player.get_or_insert(user.user_id(), user = user, pseudonym = self.request.get('pseudonym'))
    send_email(user, "Welcome to OPONGER, %s!" % (player.pseudonym), "We'll be in contact regarding your games.")
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

from google.appengine.api import mail
def send_email(user, subject, body):
  # TODO: create an opongersupport@opower.com user, give the Admin access to the Google App, and change the sender to that
  # For detils, see: http://www.pressthered.com/solving_invalidsendererror_unauthorized_sender_in_appengine/
  mail.send_mail(
      sender="OPONGER Support <yoni.ben-meshulam@opower.com>",
      to = user.email(),
      subject = subject,
      body = body)

application = webapp.WSGIApplication(
  [('/', MainPage),
  ('/signup', SignUp),
  ('/update_player', UpdatePlayer)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

