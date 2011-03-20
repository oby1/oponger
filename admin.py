"""
Handles pages which are admin-only access. See app.py for the URL mapping.
"""
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


from lib.admin_handlers import MainPage, UpdateSchema


application = webapp.WSGIApplication(
  [('/admin/', MainPage),
   ('/admin/update_schema', UpdateSchema)],
  debug=True)

def main():
  logging.getLogger().setLevel(logging.DEBUG)
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
