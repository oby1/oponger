from google.appengine.ext import db

class Player(db.Model):
  date = db.DateTimeProperty(auto_now_add=True)
  pseudonym = db.StringProperty(required=True)
  user = db.UserProperty(required=True)
