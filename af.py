from scapy.all import *


def send_packet(packet):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 8000))
        s.send(bytes(packet[Raw]))
        print("Request Sent!")
    except Exception as e:
        print(e)


def read_pcap(path: str):
    scapy_cap = rdpcap(path)
    for packet in scapy_cap:
        if packet[IP].src == '10.100.233.89' and Raw in packet:
            # breakpoint()
            send_packet(packet)
            break  # TODO: For now


if __name__ == '__main__':
    read_pcap('invite-filtered.pcap')
