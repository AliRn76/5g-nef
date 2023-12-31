from scapy.all import *

scapy_cap = rdpcap('pcrf-diameter.pcap')
for packet in scapy_cap:
    breakpoint()

