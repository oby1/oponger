from google.appengine.ext import db
# Terrible implementation for DC and SF locations, but good enough to get things going

DC = {
  'name'  : 'DC',
  'geoPt' : db.GeoPt(lat=38.896861, lon=-77.095077)
}

SF = {
  'name'  : 'SF',
  'geoPt' : db.GeoPt(lat=37.779339, lon=-122.393349)
}

LOCATIONS = [DC, SF]

