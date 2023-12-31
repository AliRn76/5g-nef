import requests

url = '/nudr-dr/v1/policy-data/ues/imsi-999990000000031/sm-data?dnn=internet&snssai=%7B%0A%09%22sst%22%3A%091%0A%7D'

headers = {
    ':authority': 'core5g-udr',
    'accept': 'application/json,application/problem+json',
    '3gpp-sbi-sender-timestamp': ...,  # Sun, 31 Dec 2023 07:04:29.061 GMT
    '3gpp-sbi-max-rsp-time': ...,  # 10000
    'user-agent': 'PCF',
}

response = requests.get(url=url, headers=headers)
print(response.status_code, response.content)

