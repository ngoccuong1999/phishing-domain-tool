import requests
import json
import csv
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

with open('ip_phishing.csv') as csv_file:
    url = 'https://127.0.0.1:8443/api/v1/firewall/rule'
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
# list address IP hien co de xem co trung khong
    payload = {
        "client-id": "admin",
        "client-token": "pfsense"
    }
    response = requests.get(url, verify=False, json=payload)
    data = response.json()
    # js = json.dumps(data, indent=4)
    # print(js)
# chay de lay tung IP va nem vao trong list ip
    currentIpList = []
    for i in data["data"]:
        ipTemp = i["source"].get("address", 0)
        if ipTemp != 0:
            currentIpList.append(ipTemp)
    # print(currentIpList)

    for row in csv_reader:
        # print(row)
        if line_count == 0:
            ipPosition = 0
# tim vi tri cot ip
            for columeName in row:
                if columeName == 'ip':
                    break
                ipPosition += 1
            # print("Ip position: ", ipPosition)
            line_count += 1
        else:
            ip = row[ipPosition]
# kiem tra ip nay da co trong firewall hay chua
            check = 0
            for existIp in currentIpList:
                if ip == existIp:
                    check = 1
                    break
            if check != 1:
                payload = {
                    "client-id": "admin",
                    "client-token": "pfsense",
                    "type": "block",
                    "interface": "wan",
                    "ipprotocol": "inet",
                    "protocol": "tcp",
                    "src": ip,
                    "srcport": "any",
                    "dst": "vtnet0",
                    "dstport": 443,
                    "descr": "This is a test rule added via API",
                    "top": True
                }
                response = requests.post(url, verify=False, json=payload)
                # print(response.content)
            line_count += 1

# Auto apply change firewall rule
urlApply = 'https://127.0.0.1:8443/api/v1/firewall/apply'
payload = {

}
response = requests.post(urlApply, verify=False, json=payload)


# reference
# https://stackoverflow.com/questions/15445981/how-do-i-disable-the-security-certificate-check-in-python-requests
