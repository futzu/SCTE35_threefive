"""
The reader function
"""

import socket
import struct
import urllib.request


def reader(uri):
    """
    reader returns an open file handle.

    files:              "/home/you/video.ts"
    http(s) urls:       "https://example.com/vid.ts"
    udp urls:           "udp://1.2.3.4:5555"
    multicast urls:     "udp://@227.1.3.10:4310"



    Use like:

    with reader("udp://@227.1.3.10:4310") as data:
        data.read(8192)

    with reader("/home/you/video.ts") as data:
        fu = data.read()

    udp_data =reader("udp://1.2.3.4:5555")
    chunks = [udp_data.read(188) for i in range(0,1024)]
    udp_data.close()



    """
    # Multicast
    if uri.startswith("udp://@"):
        return open_mcast(uri)
    # Udp
    if uri.startswith("udp://"):
        return open_udp(uri)
    # Http(s)
    if uri.startswith("http"):
        return urllib.request.urlopen(uri)
    # File
    return open(uri, "rb")


def read_stream(sock):
    """
    return a socket that can be read like a file.
    """
    return sock.makefile(mode="rb")


def _mk_udp_sock(udp_ip, udp_port):
    """
    udp socket setup
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))
    return sock


def _mk_mcast_sock(mcast_grp, mcast_port, all_grps=True):
    """
    multicast socket setup
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 212992)

    if all_grps:
        sock.bind(("", mcast_port))
    else:
        sock.bind((mcast_grp, mcast_port))
    mreq = struct.pack("4sl", socket.inet_aton(mcast_grp), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock


def open_udp(uri):
    """
    udp://1.2.3.4:5555
    """
    udp_ip, udp_port = (uri.split("udp://")[1]).split(":")
    udp_port = int(udp_port)
    udp_sock = _mk_udp_sock(udp_ip, udp_port)
    return read_stream(udp_sock)


def open_mcast(uri):
    """
    udp://@227.1.3.10:4310
    """
    mcast_grp, mcast_port = (uri.split("udp://@")[1]).split(":")
    mcast_port = int(mcast_port)
    mcast_sock = _mk_mcast_sock(mcast_grp, mcast_port)
    return read_stream(mcast_sock)
