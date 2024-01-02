import json
from collections import defaultdict

import httpx
from pyDiameter.pyDiaMessage import DiaMessage

FLOW_STATUSES = ['ENABLED-UPLINK', 'ENABLED-DOWNLINK', 'ENABLED', 'DISABLED', 'REMOVED']
FLOW_USAGES = ['NO_INFO', 'RTCP', 'AF_SIGNALLING']
MED_TYPE = ['AUDIO', 'VIDEO', 'DATA', 'APPLICATION', 'CONTROL', 'TEXT', 'MESSAGE', 'OTHER']

UE_IP = '10.45.0.10'

HTTP_CLIENT = httpx.Client(http1=False, http2=True)


def send_to_pcf(data):
    url = 'http://127.0.0.1:8000/npcf-policyauthorization/v1/app-sessions'

    if 'Media-Component-Description' not in data:
        print('Does not have "Media-Component-Description"')
        return

    codec = [c[:-1].decode() for c in data['Media-Component-Description']['Codec-Data AVP']]
    media_component = data['Media-Component-Description']
    payload = {
        'ascReqData': {
            'ueIpv4': UE_IP,
            'afAppId': data['AF-Application-Identifier'].decode(),
            'codecs': codec,
            'ipv4Addr': '192.168.10.10',
            'notifUri': 'https://google.com',
            'suppFeat': '',
            'medComponents': {
                '0': {
                    'medCompN': media_component['Media-Component-Number'],
                    'marBwDl': str(media_component['Max-Requested-Bandwidth-DL']),
                    'marBwUl': str(media_component['Max-Requested-Bandwidth-UL']),
                    'fStatus': FLOW_STATUSES[media_component['Flow-Status']],
                    'medType': MED_TYPE[media_component['Media-Type']],
                    'medSubComps': {
                        '0': {
                            'fNum': media_component['Media-Sub-Component']['Flow-Number'],
                            'flowUsage': FLOW_USAGES[media_component['Media-Sub-Component']['Flow-Usage']]
                        }
                    }
                }
            }

        }
    }
    # breakpoint()

    response = HTTP_CLIENT.post(url=url, json=payload)
    if response.status_code == 201:
        print(json.loads(response.text))
    else:
        print(f'Failed {response.content=}, {response.status_code=}')


def parse_avp(avp):
    avp_dict = defaultdict(dict)

    name = avp.getAVPName()
    value = avp.getAVPValue()

    if isinstance(value, list):
        for sub in value:
            sub_avp = parse_avp(sub)
            for k, v in sub_avp.items():
                if k in avp_dict[name]:
                    avp_dict[name][k] = [avp_dict[name][k], v]
                else:
                    avp_dict[name][k] = v
    else:
        avp_dict[name] = value
    return avp_dict


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
    server.bind(('127.0.0.1', 8001))
    server.listen()

    while True:
        communication_socket, address = server.accept()
        message = communication_socket.recv(8192)
        avps = parse_diameter(message)
        communication_socket.close()

        print('\n-----------------------------------\n')
        send_to_pcf(avps)
        # pprint(avps)


if __name__ == '__main__':
    listen()
