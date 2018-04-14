#/email/Email.py
import smtplib, config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Emailer():
    def __init__(self):
        self.server = smtplib.SMTP(config.EMAIL_SERVER, config.EMAIL_PORT)
        self.server.starttls()
        print("Server Setup")
        self.server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)

    def send_email(self, message):
        """Sends a MIMEMulipart Message"""
        message['From'] = config.EMAIL_PASSWORD
        self.server.send_message(message, config.EMAIL_PASSWORD, message['To'])
        print("Email Sent")

#TEST
# msg = MIMEMultipart()
# msg['From'] = config.EMAIL_ADDRESS
# msg['To'] = "jamieluckett@gmail.com"
# msg['Subject'] = "subject"
# text = MIMEText("TEST", "text")
# html = MIMEText("<h1>TEST</h1>", "html")
# msg.attach(html)
#
# e = Emailer()
# e.send_email(msg)