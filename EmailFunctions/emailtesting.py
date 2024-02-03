import smtplib
from email.mime.text import MIMEText
import markdown2

sender_email = "ruthvikkonduru29@gmail.com"
sender_password = "dkcd ivkw ngmi xokf"
recipient_email = "ruthvikkonduru29@gmail.com"

body = """
<html>
  <body>
    <p>This is an <b>HTML</b> email sent from Python using the Gmail SMTP server.</p>
  </body>
</html>
"""

"""
subject = "Hello from Python"
html_message = MIMEText(body, 'html')
html_message['Subject'] = subject
html_message['From'] = sender_email
html_message['To'] = recipient_email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
   server.login(sender_email, sender_password)
   server.sendmail(sender_email, recipient_email, html_message.as_string())
"""

def send_email(content):
  # creates SMTP session
  s = smtplib.SMTP('smtp.gmail.com', 587)
  # start TLS for security
  s.starttls()
  # Authentication
  s.login(sender_email, sender_password)
  # message to be sent
  html_message = MIMEText(content, 'html')
  # sending the mail
  s.sendmail(sender_email, recipient_email, html_message.as_string())
  # terminating the session
  s.quit()