"""
The reader function
"""

import socket
import struct
import urllib.request


def reader(uri):
    """
    reader returns an open file handle
    for files or http(s) urls
    """
    if uri.startswith("udp://@"):
        return open_mcast(uri)
    if uri.startswith("http"):
        return urllib.request.urlopen(uri)
    return open(uri, "rb")



def read_stream(sock):
    return sock.makefile(mode="rb")


def mk_sock(mcast_grp, mcast_port, ALL_GROUPS=True):
    """
    multicast socket setup
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if ALL_GROUPS:
        sock.bind(("", mcast_port))
    else:
        # on this port, listen ONLY to mcast_group
        sock.bind((mcast_grp, mcast_port))
    mreq = struct.pack("4sl", socket.inet_aton(mcast_grp), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock

def open_mcast(uri):
    '''
    udp://@227.1.3.10:4310
    '''
    mcast_grp,mcast_port= (uri.split('@')[1]).split(':')
    mcast_port = int(mcast_port)
    mcast_sock = mk_sock(mcast_grp, mcast_port)
    return  read_stream(mcast_sock)
