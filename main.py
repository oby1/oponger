from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import os
from google.appengine.ext.webapp import template


class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    players = db.GqlQuery("SELECT * FROM Player ORDER BY date DESC")

    if user:
      template_values = {
        'nickname': user.nickname(),
        'players' : players,
      }
      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))
                              
    else:
      self.redirect(users.create_login_url(self.request.uri))

class SignUp(webapp.RequestHandler):
  def post(self):
    player = Player(pseudonym=self.request.get('pseudonym'))
    if users.get_current_user():
      player.user = users.get_current_user()
    player.put()
    self.redirect('/')

class Player(db.Model):
  user = db.UserProperty()
  pseudonym = db.StringProperty(multiline=True, required=True)
  date = db.DateTimeProperty(auto_now_add=True)

application = webapp.WSGIApplication(
  [('/', MainPage),
  ('/signup', SignUp)],
  debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

