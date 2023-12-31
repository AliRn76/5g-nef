import random
from collections import defaultdict
from datetime import datetime

import requests
from pyDiameter.pyDiaMessage import DiaMessage


def send_to_pcf():
    n = random.randint(100, 999)
    url = f'/nudr-dr/v1/policy-data/ues/imsi-999990000000{n}/sm-data?dnn=internet&snssai=%7B%0A%09%22sst%22%3A%091%0A%7D'
    timestamp = datetime.utcnow().strftime('%a, %d %b %Y %I:%M:%S:%f GMT')
    headers = {
        ':authority': 'core5g-udr',
        'accept': 'application/json,application/problem+json',
        '3gpp-sbi-sender-timestamp': timestamp,
        '3gpp-sbi-max-rsp-time': 10000,
        'user-agent': 'PCF',
    }

    response = requests.get(url=url, headers=headers)
    print(response.status_code, response.content)


def parse_avp(avp):
    avps = defaultdict(dict)

    value = avp.getAVPValue()
    if isinstance(value, list):
        for sub in value:
            avps[avp.getAVPName()].update(parse_avp(sub))
    else:
        avps[avp.getAVPName()] = value
    return avps


def parse_diameter(message):
    msg = DiaMessage()
    msg.decode(message)
    final_avps = {}
    for avp in msg.getAVPs():
        final_avps.update(parse_avp(avp))

    return final_avps


def listen():
    import socket

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8000))
    server.listen()

    while True:
        communication_socket, address = server.accept()
        message = communication_socket.recv(8192)
        avps = parse_diameter(message)
        communication_socket.close()

        from pprint import pprint
        pprint(avps)


if __name__ == '__main__':
    listen()
