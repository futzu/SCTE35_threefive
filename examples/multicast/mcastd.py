import socket
import sys

"""
This script streams a local video file
via multicast on the loopback interface.

Start multicast stream:

    python3 mcastd.py video.ts

Start the client(in a new terminal):

    python3 mcastc.py
    
"""

mcast_ip = "224.255.0.1"
mcast_port = 35555
ttl = b"\x01"
packet_size = 1316
multicast_group = (mcast_ip, mcast_port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

with open(sys.argv[1], "rb") as message:
    while message:
        sock.sendto(message.read(packet_size), multicast_group)
    sock.close()
    sys.exit()
