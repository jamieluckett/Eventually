#email_system.py
#To be run constantly on the server

import threading
from datetime import datetime
import config, generate_email
from Emailer import Emailer

def email_loop():
    threading.Timer(config.EMAIL_LOOP_INTERVAL, email_loop).start()
    emails = generate_email.generate_all_email()
    print(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
    print("Emails Generated -", len(emails))
    if len(emails) > 0:
        EmailSystem = Emailer()
        for email in emails:
            EmailSystem.send_email(email)
        print()
    else:
        print()

if __name__ == "__main__":
    print("== email_system.py ==")
    print("Configured to run loop every %s second(s)"%(config.EMAIL_LOOP_INTERVAL))
    email_loop()