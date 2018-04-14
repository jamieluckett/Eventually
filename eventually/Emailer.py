#/email/Email.py
import smtplib, config
from socket import socket


class Emailer():
    def __init__(self):
        try:
            self.server = smtplib.SMTP(config.EMAIL_SERVER, config.EMAIL_PORT)
            self.server.starttls()
            self.server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
            self.setup = True
        except socket.error as e:
            print(e)
            self.setup = False


    def send_email(self, message):
        """Sends a MIMEMulipart Message"""
        if self.setup:
            message['From'] = config.EMAIL_PASSWORD
            self.server.send_message(message, config.EMAIL_PASSWORD, message['To'])
            print("Email Sent")
        else:
            print("Emailer failed to setup")

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