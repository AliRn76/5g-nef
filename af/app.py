import logging
import socket
import time
from typing import Iterator

from scapy.layers.inet import IP
from scapy.packet import Raw
from scapy.utils import rdpcap

logger = logging.getLogger()


class AF:
    NEF_IP = 'nef-service.hc-core-1.cluster.local'
    NEF_PORT = 8000

    def __init__(self, pcap_path: str):
        self.pcap_path = pcap_path

    def read_pcap(self) -> Iterator[Raw]:
        """Read And Filter Packets of PcapFile"""
        for packet in rdpcap(self.pcap_path):
            if packet[IP].src == '10.100.233.89' and Raw in packet:
                yield packet[Raw]

    @classmethod
    def send_packet_to_nef(cls, raw_data: Raw):
        """Send a Packet To NEF"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((cls.NEF_IP, cls.NEF_PORT))
            s.send(bytes(raw_data))
            logger.info('Request Sent!')
        except Exception as e:
            logger.error(e)
        finally:
            s.close()


if __name__ == '__main__':
    af = AF(pcap_path='af/diameters.pcap')
    while True:
        for packet in af.read_pcap():
            time.sleep(1)  # For Test
            af.send_packet_to_nef(packet)
        time.sleep(5)  # For Test
