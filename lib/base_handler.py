import logging
import os

# Django 1.2 gives better templating
# see http://code.google.com/p/googleappengine/source/browse/trunk/python/google/appengine/ext/webapp/template.py#53
from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api.users import create_logout_url

from models import Player
from locations import LOCATIONS


"""Templates live in this path-relative directory."""
PATH_TO_TEMPLATES = os.path.join(os.path.dirname(__file__),"../templates")

register = template.register_template_library('templatetags.gravatar')

class BaseHandler(webapp.RequestHandler):
  """
  A handler that does common things, such as retrieving the current user.
  Follows the Template pattern, as described in:
  http://stackoverflow.com/questions/4488015/google-app-engine-define-a-preprocessing-class
  """
  def __init__(self):
    self.user = users.get_current_user()
    # Creates a player if one does not already exist. No signup required!
    self.player = Player.get_or_insert(self.user.user_id(), user = self.user, pseudonym = self.user.nickname())
    self.template_values = {
          'user'          : self.user,
          'player'        : self.player,
          'logout_url'    : create_logout_url('/'),
          'locations'     : LOCATIONS,
        }
    logging.debug("Setting up template values %s" % (self.template_values))

  def setup(self):
    # Used for all forms on a page, to specify where to redirect back after form submission
    # see redirect_to_redirect_path_or_home
    self.template_values['redirect_path'] = self.request.path
    try:
      self.template_values['is_admin'] = self.request._environ['USER_IS_ADMIN']
    except:
      self.template_values['is_admin'] = False

  def get(self, *args):
    self.setup()
    # call the derived class' 'DoGet' method that actually has
    # the logic inside it
    self.DoGet(*args)

  def post(self, *args):
    self.setup()
    # call the derived class' 'DoPost' method
    logging.debug("POST request body: %s" % self.request.body)
    self.DoPost(*args)

  def redirect_to_redirect_path_or_home(self):
    redirect_path = self.request.get('redirect_path')
    self.redirect(redirect_path if redirect_path else '/')

  def render_to_response(self, template_name):
    """
    Opens the given template and renders the values to the response,
    along with the resulting template_values.
    """
    path = os.path.join(PATH_TO_TEMPLATES, template_name)
    logging.debug("Rendering template_values %s to template %s." % (self.template_values, template_name))
    self.response.out.write(template.render(path, self.template_values))
