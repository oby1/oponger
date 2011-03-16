from google.appengine.ext import db
from locations import DC

class Player(db.Model):
  date = db.DateTimeProperty(auto_now_add=True)
  pseudonym = db.StringProperty(required=True)
  user = db.UserProperty(required=True)
  location = db.GeoPtProperty(default=DC['geoPt'])

