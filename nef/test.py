from unittest import TestCase

from nef.app import Diameter


class TestNef(TestCase):
    def test_parse_diameter(self):
        sample_diameter = b'\x01\x00\x08l\xc0\x00\x01\t\x01\x00\x00\x14\x08\x98\xe2\x85\x010\xaf\xda\x00\x00\x01\x07@\x00\x00=pcscf.ims.mnc001.mcc001.3gppnetwork.org;2969444371;11\x00\x00\x00\x00\x00\x01\x08@\x00\x00/pcscf.ims.mnc001.mcc001.3gppnetwork.org\x00\x00\x00\x01(@\x00\x00)ims.mnc001.mcc001.3gppnetwork.org\x00\x00\x00\x00\x00\x01\x02@\x00\x00\x0c\x01\x00\x00\x14\x00\x00\x01\x04@\x00\x00 \x00\x00\x01\n@\x00\x00\x0c\x00\x00(\xaf\x00\x00\x01\x02@\x00\x00\x0c\x01\x00\x00\x14\x00\x00\x01\x1b@\x00\x00)epc.mnc001.mcc001.3gppnetwork.org\x00\x00\x00\x00\x00\x01\xf8\xc0\x00\x00\x18\x00\x00(\xafIMS Services\x00\x00\x01#@\x00\x00\x0c\x00\x00\x8c\xa0\x00\x00\x01\xbb@\x00\x00D\x00\x00\x01\xc2@\x00\x00\x0c\x00\x00\x00\x02\x00\x00\x01\xbc@\x00\x00.sip:001010000031532@192.168.101.2:6500\x00\x00\x00\x00\x01\xca\x80\x00\x00\x10\x00\x002\xdb\x00\x00\x00\x00\x00\x00\x02\x05\xc0\x00\x06X\x00\x00(\xaf\x00\x00\x02\x06\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x01\x00\x00\x02\x07\xc0\x00\x01T\x00\x00(\xaf\x00\x00\x01\xfd\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x01\x00\x00\x01\xfb\xc0\x00\x00I\x00\x00(\xafpermit out 17 from 192.168.10.104 49152 to 192.168.101.2 1234\x00\x00\x00\x00\x00\x01\xfb\xc0\x00\x00H\x00\x00(\xafpermit in 17 from 192.168.101.2 1234 to 192.168.10.104 49152\x00\x00\x01\xfb\xc0\x00\x00I\x00\x00(\xafpermit out 17 from 192.168.10.104 49153 to 192.168.101.2 1235\x00\x00\x00\x00\x00\x01\xfb\xc0\x00\x00H\x00\x00(\xafpermit in 17 from 192.168.101.2 1235 to 192.168.10.104 49153\x00\x00\x02\x00\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x00\x00\x00\x02\x08\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x00\x00\x00\x02\x04\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\xa4\x10\x00\x00\x02\x03\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\xa0(\x00\x00\x02\x0c\xc0\x00\x03\x11\x00\x00(\xafdownlink\noffer\nm=audio 49152 RTP/AVP 112 104 107 118 96 111 110\r\nb=AS:42\r\nb=RS:0\r\nb=RR:2500\r\na=curr:qos local none\r\na=curr:qos remote none\r\na=des:qos mandatory local sendrecv\r\na=des:qos optional remote sendrecv\r\na=maxptime:240\r\na=rtpmap:112 EVS/16000\r\na=fmtp:112 br=5.9-24.4;bw=nb-swb;ch-aw-recv=3\r\na=rtpmap:104 AMR-WB/16000/1\r\na=fmtp:104 mode-change-capability=2;max-red=220\r\na=rtpmap:107 AMR-WB/16000/1\r\na=fmtp:107 octet-align=1;mode-change-capability=2;max-red=220\r\na=rtpmap:118 AMR/8000/1\r\na=fmtp:118 mode-change-capability=2;max-red=220\r\na=rtpmap:96 AMR/8000/1\r\na=fmtp:96 octet-align=1;mode-change-capability=2;max-red=220\r\na=rtpmap:111 telephone-event/16000\r\na=fmtp:111 0-15\r\na=rtpmap:110 telephone-event/8000\r\na=fmtp:110 0-15\r\na=sendrecv\r\na=rtcp:49153\r\na=ptime:20\r\n\x00\x00\x00\x00\x00\x00\x02\x0c\xc0\x00\x01\x91\x00\x00(\xafuplink\nanswer\nm=audio 1234 RTP/AVP 104 111\r\nb=AS:41\r\nb=RS:0\r\nb=RR:0\r\na=rtpmap:104 AMR-WB/16000/1\r\na=fmtp:104 mode-change-capability=2;max-red=220\r\na=rtpmap:111 telephone-event/16000\r\na=fmtp:111 0-15\r\na=ptime:20\r\na=maxptime:240\r\na=sendrecv\r\na=curr:qos local none\r\na=curr:qos remote none\r\na=des:qos mandatory local sendrecv\r\na=des:qos mandatory remote sendrecv\r\na=conf:qos remote sendrecv\r\n\x00\x00\x00\x00\x00\x00\x01\xff\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x02\x00\x00\x00\x08@\x00\x00\x0c\xc0\xa8e\x02\x00\x00\x02\x01\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x01\x00\x00\x02\x01\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x02\x00\x00\x02\x01\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x03\x00\x00\x02\x01\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x04\x00\x00\x02\x01\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x05\x00\x00\x02\x01\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x06\x00\x00\x02\x01\xc0\x00\x00\x10\x00\x00(\xaf\x00\x00\x00\x0c\x00\x00\x01\x14@\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x1b@\x00\x00\x0c\x00\x00\x8c\xa0'
        expected_avps = {
            'Session-Id': b'pcscf.ims.mnc001.mcc001.3gppnetwork.org;2969444371;11',
            'Origin-Host': b'pcscf.ims.mnc001.mcc001.3gppnetwork.org',
            'Origin-Realm': b'ims.mnc001.mcc001.3gppnetwork.org',
            'Auth-Application-Id': 16777236,
            'Vendor-Specific-Application-Id': {
                'Vendor-Id': 10415,
                'Auth-Application-Id': 16777236
            },
            'Destination-Realm': b'epc.mnc001.mcc001.3gppnetwork.org',
            'AF-Application-Identifier': b'IMS Services',
            'Authorization-Lifetime': 36000,
            'Subscription-Id': {
                'Subscription-Id-Type': 2,
                'Subscription-Id-Data': b'sip:001010000031532@192.168.101.2:6500'
            },
            'Reservation-Priority': 0,
            'Media-Component-Description': {
                'Media-Component-Number': 1,
                'Media-Sub-Component': {
                    'Flow-Number': 1,
                    'Flow-Description': [[[
                        b'permit out 17 from 192.168.10.104 49152 to 192.168.101.2 1234',
                        b'permit in 17 from 192.168.101.2 1234 to 192.168.10.104 49152'
                    ], b'permit out 17 from 192.168.10.104 49153 to 192.168.101.2 1235'
                    ], b'permit in 17 from 192.168.101.2 1235 to 192.168.10.104 49153'],
                    'Flow-Usage': 0
                },
                'Media-Type': 0,
                'Max-Requested-Bandwidth-UL': 42000,
                'Max-Requested-Bandwidth-DL': 41000,
                'Codec-Data AVP': [
                    b'downlink\n'
                    b'offer\n'
                    b'm=audio 49152 RTP/AVP 112 104 107 118 96 111 110\r\n'
                    b'b=AS:42\r\n'
                    b'b=RS:0\r\n'
                    b'b=RR:2500\r\n'
                    b'a=curr:qos local none\r\n'
                    b'a=curr:qos remote none\r\n'
                    b'a=des:qos mandatory local sendrecv\r\n'
                    b'a=des:qos optional remote sendrecv\r\n'
                    b'a=maxptime:240\r\n'
                    b'a=rtpmap:112 EVS/16000\r\n'
                    b'a=fmtp:112 br=5.9-24.4;bw=nb-swb;ch-aw-recv=3\r\n'
                    b'a=rtpmap:104 AMR-WB/16000/1\r\n'
                    b'a=fmtp:104 mode-change-capability=2;max-red=220\r\n'
                    b'a=rtpmap:107 AMR-WB/16000/1\r\n'
                    b'a=fmtp:107 octet-align=1;mode-change-capability=2;max-red=220\r\n'
                    b'a=rtpmap:118 AMR/8000/1\r\n'
                    b'a=fmtp:118 mode-change-capability=2;max-red=220\r\n'
                    b'a=rtpmap:96 AMR/8000/1\r\n'
                    b'a=fmtp:96 octet-align=1;mode-change-capability=2;max-red=220\r\n'
                    b'a=rtpmap:111 telephone-event/16000\r\n'
                    b'a=fmtp:111 0-15\r\n'
                    b'a=rtpmap:110 telephone-event/8000\r\n'
                    b'a=fmtp:110 0-15\r\n'
                    b'a=sendrecv\r\n'
                    b'a=rtcp:49153\r\n'
                    b'a=ptime:20\r\n'
                    b'\x00',
                    b'uplink\n'
                    b'answer\n'
                    b'm=audio 1234 RTP/AVP 104 111\r\n'
                    b'b=AS:41\r\n'
                    b'b=RS:0\r\n'
                    b'b=RR:0\r\n'
                    b'a=rtpmap:104 AMR-WB/16000/1\r\n'
                    b'a=fmtp:104 mode-change-capability=2;max-red=220\r\n'
                    b'a=rtpmap:111 telephone-event/16000\r\n'
                    b'a=fmtp:111 0-15\r\n'
                    b'a=ptime:20\r\n'
                    b'a=maxptime:240\r\n'
                    b'a=sendrecv\r\n'
                    b'a=curr:qos local none\r\n'
                    b'a=curr:qos remote none\r\n'
                    b'a=des:qos mandatory local sendrecv\r\n'
                    b'a=des:qos mandatory remote sendrecv\r\n'
                    b'a=conf:qos remote sendrecv\r\n'
                    b'\x00'
                ],
                'Flow-Status': 2
            },
            'Framed-IP-Address': b'\xc0\xa8e\x02',
            'Specific-Action': 12,
            'Auth-Grace-Period': 0,
            'Session-Timeout': 36000
        }

        diameter = Diameter(sample_diameter)
        assert diameter.avps.keys() == expected_avps.keys()
        for k, v in diameter.avps.items():
            assert expected_avps[k] == v
