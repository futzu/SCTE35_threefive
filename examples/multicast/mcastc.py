from functools import partial
import socket
import sys
from threefive import Stream

"""
See README.txt
"""


def foundit(cue):
    """
    for custom SCTE-35 cue data handling
    pass a function in to Stream.decode.

    example:
            Stream.decode(func=foundit)
    """
    cue.to_stderr()


def read_stream(sock):
    with sock.makefile(mode="rb") as socket_file:
        ts = Stream(socket_file, show_null=True)
        ts.decode(func=foundit)
        # ts.show()   # will display stream types by program.


def mk_sock(mcast_host, mcast_ip, mcast_port):
    """
    multicast socket setup
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(mcast_ip) + socket.inet_aton(mcast_host),
    )
    sock.bind((mcast_host, mcast_port))
    return sock


if __name__ == "__main__":
    mcast_host = "0.0.0.0"
    mcast_ip = "239.255.0.35"
    mcast_port = 35555
    mcast_sock = mk_sock(mcast_host, mcast_ip, mcast_port)
    read_stream(mcast_sock)
