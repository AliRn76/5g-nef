from unittest import TestCase
from unittest.mock import patch

from scapy.packet import Raw

from af.app import AF


class TestAF(TestCase):

    def test_read_pcap(self):
        for packet in AF('af/diameters.pcap').read_pcap():
            assert isinstance(packet, Raw)

    @patch('socket.socket.send')
    @patch('socket.socket.connect')
    def test_send_packet(self, _connect, _send):
        def send_side_effect(data):
            assert type(data) is Raw
            assert data == bytes(first_packet)

        _send.side_effect = send_side_effect
        first_packet = list(AF('af/diameters.pcap').read_pcap())[0]
        print(bytes(first_packet))
        AF.send_packet_to_nef(first_packet)
