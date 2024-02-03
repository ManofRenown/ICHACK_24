import smtplib
from email.mime.text import MIMEText

sender_email = "ruthvikkonduru29@gmail.com"
sender_password = "dkcd ivkw ngmi xokf"
recipient_email = "ruthvikkonduru29@gmail.com"


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