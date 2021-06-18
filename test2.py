import requests
import json
import csv
import pandas as pd
from ratelimit import limits, sleep_and_retry
import smtplib, ssl
# rate limit call api 20 calls per minute

CALLS = 20
RATE_LIMIT = 60 # second
@sleep_and_retry
@limits(calls=CALLS, period= RATE_LIMIT)
def check_limit():
    '''Empty function just to check for calls to API'''
    return
#Send email, source: https://realpython.com/python-send-email/
message = """Subject: New Phishing Domain 


Hi {name}

Domain {domain} with ip: {ip}
Record: {record}
first_seen: {first_seen}
last_seen: {last_seen}
source: {source}

Good luck!
"""


smtp_server = "smtp.gmail.com"
port = 587 # for start TLS
sender_email = "crosslinevn@gmail.com"
password = "6vyVtfJUWr8WjEc"
# Create a secure SSL context
context = ssl.create_default_context()
#Try to log in to server and send email
try: 
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls(context=context) # secure the connection
    server.ehlo() # Can be omitted
    server.login(sender_email, password)
    #Send email here
    with open("contacts_file.csv") as receiver_email:
        reader = csv.reader(receiver_email)
        next(reader) #skip header row
        for name, email in reader:
            print(email)
            server.sendmail(sender_email, email, message)
except Exception as e:
    #Print any error messages to stdout
    print(e)
finally:
    server.quit()
