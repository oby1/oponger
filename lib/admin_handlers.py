from lib.base_handler import BaseHandler

class UpdateSchema(BaseHandler):
  def DoGet(self):
    self.render_to_response("update_schema.html")
