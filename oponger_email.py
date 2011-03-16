from google.appengine.api import mail

def send_email(user, subject, body):
  """Sends an email to the given user, with the provided subject and body."""
  # TODO: create an opongersupport@opower.com user, give the Admin access to the Google App, and change the sender to that
  # For detils, see: http://www.pressthered.com/solving_invalidsendererror_unauthorized_sender_in_appengine/
  mail.send_mail(
      sender="OPONGER Support <yoni.ben-meshulam@opower.com>",
      to = user.email(),
      subject = subject,
      body = body)
