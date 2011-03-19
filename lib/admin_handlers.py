from lib.base_handler import BaseHandler
from lib.models import Player


class MainPage(BaseHandler):
  def DoGet(self):
    self.render_to_response("admin_index.html")

class UpdateSchema(BaseHandler):
  def DoGet(self):
    # By loading and storing each player, we're updating the player for any
    # schema changes.
    # This will not work once we have more than 1000 records, but it's fine for now.
    for player in Player.all():
      player.put()
    self.render_to_response("update_schema.html")
