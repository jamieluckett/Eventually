#email_system.py
#To be run constantly on the server

import threading
import config
from Emailer import Emailer
import generate_email

def email_loop():
    threading.Timer(config.EMAIL_LOOP_INTERVAL, email_loop).start()
    print("Email Loop Start")
    emails = generate_email.generate_all_email()
    print("Emails Generated -", len(emails))
    if len(emails) > 0:
        EmailSystem = Emailer()
        for email in emails:
            EmailSystem.send_email(email)

if __name__ == "__main__":
    email_loop()