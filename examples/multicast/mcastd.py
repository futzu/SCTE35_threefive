import socket
import sys

"""
See README.txt   
"""

mcast_ip = "225.255.0.35"
mcast_port = 35555
ttl = b"\x1f"
packet_size = 188
multicast_group = (mcast_ip, mcast_port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

with open(sys.argv[1], "rb") as vid:
    while vid:
        chunk = vid.read(packet_size)
        if not chunk:
            break
        sock.sendto(chunk, multicast_group)
    sock.close()
    sys.exit()
