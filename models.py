from google.appengine.ext import db

DC = {
  'name'  : 'DC',
  'geoPt' : db.GeoPt(lat=38.896861, lon=-77.095077)
}

SF = {
  'name'  : 'SF',
  'geoPt' : db.GeoPt(lat=37.779339, lon=-122.393349)
}

LOCATIONS = [DC, SF]

class Player(db.Model):
  date = db.DateTimeProperty(auto_now_add=True)
  pseudonym = db.StringProperty(required=True)
  user = db.UserProperty(required=True)
  location = db.GeoPtProperty(default=DC['geoPt'])

