import requests
import json
import csv
import pandas as pd
from ratelimit import limits, sleep_and_retry
# rate limit call api 20 calls per minute

CALLS = 20
RATE_LIMIT = 60 # second
@sleep_and_retry
@limits(calls=CALLS, period= RATE_LIMIT)
def check_limit():
    '''Empty function just to check for calls to API'''
    return


username = "tipdemo02@vcyber.io" 
key_Api = "c8544915a01e23549372b44644d27937371761c1"

with open('ip_test.txt') as ipPhishing_list:
    #create Url
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
        print(response.status_code)
        try:
            data = response.json()
            # js = json.dumps(data,indent=4)
            # print(js)
        except:
            print("Error Json")
        pf = pd.DataFrame(data["results"])
        # print(pf['domain'])
        # loc list domain xem co bi trung hay khong
        try:
            with open(f'{ip.strip()}.csv') as ip_csv:
                listDomain = []
                csv_reader = csv.reader(ip_csv, delimiter=",")
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        domainPosition = 0
                        print("2")
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
                print(listDomain)
                for domain in pf['domain']:
                    if domain not in listDomain:
                        print(domain)

                    
        except:
            print(f"{ip.strip()}.csv chua tao do lan dau tien thay ip nay")
        pf_csv = pf.to_csv(f'{ip.strip()}.csv')
        

