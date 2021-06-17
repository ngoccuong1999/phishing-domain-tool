import requests
import os
import json

url = 'https://api.abuseipdb.com/api/v2/check'
MY_API = '1c32060ffde880e02f141ada773d8b9ec746dc0f9d5016e7431c9358e4f9f8917c39f33d6e2fcda9'
# API_KEY = os.getenv(MY_API)
headers = {
    'Key': f'{MY_API}',
    'Accept': 'application/json',
}
dataIp = open('ip.txt', 'r')
for ip in dataIp:
    ip = ip.rstrip()
    params = {
        'ipAddress': ip,
        'verbose': ''
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    try:
        js = json.dumps(data, indent=4)
    except:
        js = None
    # print(js)
    country = data["data"]["countryName"]
    fileName = country + '.txt'
    for i in data["data"]["reports"]:
        print(i["reporterCountryCode"])
        if 'VN' in i["reporterCountryCode"]:
            f = open(fileName, "a")
            f.write(ip)
            f.close()
            break
dataIp.close()
