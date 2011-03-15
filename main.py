from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import os
import sys
from google.appengine.ext.webapp import template
from models import Player

class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    players = db.GqlQuery("SELECT * FROM Player ORDER BY date DESC")

    if user:
      template_values = {
        'player'  : Player.get_by_key_name(user.user_id()),
        'nickname': user.nickname(),
        'players' : players,
      }
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
    self.redirect('/')

application = webapp.WSGIApplication(
  [('/', MainPage),
  ('/signup', SignUp)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

