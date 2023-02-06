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

Domain "{domain}" with ip:"{ip}"
Record: {record}
first_seen: {first_seen}
last_seen: {last_seen}
source: {source}

Good luck!
"""


def sendEmail(df):
    smtp_server = "smtp.gmail.com"
    port = 587 # for start TLS
    sender_email = "thanthien2kk@gmail.com"
    password = ""
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
                print(df["domain"])
                # print(name)
                # print(df["ip"])
                # print(df["rrtype"])
                         
                server.sendmail(sender_email, email, message.format(name=name, domain=df["domain"].replace(".","[.]"), ip=df["ip"], record=df["rrtype"], source=df["source"], first_seen=df["first_seen"], last_seen=df["last_seen"]))
    except Exception as e:
        #Print any error messages to stdout
        print(e)
    finally:
        server.quit()

username = "tipdemo02@vcyber.io" 
key_Api = "c8544915a01e23549372b44644d27937371761c1"
#add banner like hacker :D :D 
#https://www.devdungeon.com/content/create-ascii-art-text-banners-python
#pip install pyfiglet
import pyfiglet

with open('IP_Theo_Doi.txt') as ipPhishing_list:
    #create Url
    ascii_banner = pyfiglet.figlet_format("Crossline!!")
    print(ascii_banner)
    print("Tool created by Ngoc Cuong ver2.0 18/06/2021")
    urlInitial = "https://api.threatstream.com/api/v1/pdns/ip/"
    for ip in ipPhishing_list:
        url = urlInitial + ip 
        # print("url test:", url)
        # Goi API to threat stream passiveDNS
        header = {
            "Authorization": f"apikey {username}:{key_Api}"  
        }
        check_limit()
        response = requests.get(url.strip(), headers=header)
        # print(response.status_code)
        try:
            data = response.json()
            # js = json.dumps(data,indent=4)
            # print(js)
        except:
            print("Error Json")
        df = pd.DataFrame(data["results"])
        # print(df)
        # print(df['domain'])
        # loc list domain xem co bi trung hay khong
        # print(type(df['domain']))
        check = 0 # check file change or not? if change we do write file if not, we don't write file
        start = 0 # check file is existed? 
        try:
            with open(f'{ip.strip()}.csv') as ip_csv:
                start = 1
                listDomain = []
                csv_reader = csv.reader(ip_csv, delimiter=",")
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        domainPosition = 0
                        # print("2")
                        #tim vi tri cot domain
                        for columeName in row:
                            if columeName == 'domain':
                                break
                            domainPosition += 1
                        line_count += 1
                    else:
                        domain = row[domainPosition]
                        # add domain vao list Domain de check
                        listDomain.append(domain)
                        line_count += 1
                # print(listDomain)
                count = 0
                for domain in df["domain"]:
                    if domain not in listDomain:
                        check = 1
                        print("Send email:", count)
                        sendEmail(df.loc[count])
                    count += 1

                    
        except:
            print(f"{ip.strip()}.csv chua tao do lan dau tien thay ip nay")

        if check == 1 or start == 0:
            df_csv = df.to_csv(f'{ip.strip()}.csv')
        

