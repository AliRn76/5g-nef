import json
import logging
import socket
from collections import defaultdict

import httpx
from pyDiameter.pyDiaAVPBase import DiaAVP
from pyDiameter.pyDiaMessage import DiaMessage

logger = logging.getLogger()


class Diameter:
    def __init__(self, diameter: bytes):
        self.diameter = diameter
        self.avps = {}
        self._parse_diameter()

    def _parse_diameter(self):
        """Parse Diameter Message"""
        msg = DiaMessage()
        msg.decode(self.diameter)
        for avp in msg.getAVPs():
            self.avps.update(self._parse_avp(avp))

    def _parse_avp(self, avp: DiaAVP) -> dict:
        """Parse Diameter AVPs"""
        avp_dict = defaultdict(dict)

        name = avp.getAVPName()
        value = avp.getAVPValue()

        if isinstance(value, list):
            for sub in value:
                sub_avp = self._parse_avp(sub)
                for k, v in sub_avp.items():
                    if k in avp_dict[name]:
                        avp_dict[name][k] = [avp_dict[name][k], v]
                    else:
                        avp_dict[name][k] = v
        else:
            avp_dict[name] = value
        return avp_dict


class Nef:
    UE_IP = '10.45.0.13'
    PCF_IP = 'http://127.0.0.1:8000'
    LISTEN_PORT = 8000

    FLOW_STATUSES = ['ENABLED-UPLINK', 'ENABLED-DOWNLINK', 'ENABLED', 'DISABLED', 'REMOVED']
    FLOW_USAGES = ['NO_INFO', 'RTCP', 'AF_SIGNALLING']
    MED_TYPE = ['AUDIO', 'VIDEO', 'DATA', 'APPLICATION', 'CONTROL', 'TEXT', 'MESSAGE', 'OTHER']

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.http_client = httpx.Client(http1=False, http2=True)

    def listen(self):
        """Listen for Diameter message on specific port"""
        self.server.bind(('0.0.0.0', self.LISTEN_PORT))
        self.server.listen()

        while True:
            s, address = self.server.accept()
            message = s.recv(8192)
            s.close()

            logger.info(f'Received Message From {address}')
            diameter = Diameter(diameter=message)
            self.send_to_pcf(avps=diameter.avps)

    def send_to_pcf(self, avps: dict):
        """Send Received Diameter.AVPs To PCF"""
        url = f'{self.PCF_IP}/npcf-policyauthorization/v1/app-sessions'

        if 'Media-Component-Description' not in avps:
            logger.warning('Does not have "Media-Component-Description"')
            return

        media_component = avps['Media-Component-Description']
        codec = [c[:-1].decode() for c in media_component['Codec-Data AVP']]

        payload = {
            'ascReqData': {
                'ueIpv4': self.UE_IP,
                'afAppId': avps['AF-Application-Identifier'].decode(),
                'codecs': codec,
                'ipv4Addr': '192.168.10.10',
                'notifUri': 'https://google.com',
                'suppFeat': '',
                'medComponents': {
                    '0': {
                        'medCompN': media_component['Media-Component-Number'],
                        'marBwDl': str(media_component['Max-Requested-Bandwidth-DL']),
                        'marBwUl': str(media_component['Max-Requested-Bandwidth-UL']),
                        'fStatus': self.FLOW_STATUSES[media_component['Flow-Status']],
                        'medType': self.MED_TYPE[media_component['Media-Type']],
                        'medSubComps': {
                            '0': {
                                'fNum': media_component['Media-Sub-Component']['Flow-Number'],
                                'flowUsage': self.FLOW_USAGES[media_component['Media-Sub-Component']['Flow-Usage']]
                            }
                        }
                    }
                }
            }
        }

        try:
            response = self.http_client.post(url=url, json=payload)
        except httpx.ConnectError as e:
            logger.error(f'Sending Req Failed: {e}')
        else:
            if response.status_code == 201:
                logger.info(json.loads(response.text))
            else:
                logger.error(f'Failed {response.content=}, {response.status_code=}')


if __name__ == '__main__':
    nef = Nef()
    nef.listen()
