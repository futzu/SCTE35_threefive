import socket
import threefive
import struct
import io

class TSScte35Parser():
    # TODO: Add unicast / multicast flag or auto-detect based on IP CIDR
    def __init__(self, mcast_ip, if_ip="0.0.0.0", hostname="0.0.0.0", port=9000):
        self.HOST = hostname
        self.PORT = port
        self.MCAST_IP = mcast_ip
        self.IF_IP = if_ip


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            self.set_socket_options(sock)
            sock.bind((self.HOST, self.PORT))

            with sock.makefile(mode="b") as socket_file:
                while True:
                    try:
                        scte = threefive.Stream(socket_file).decode_next()
                        if scte:
                            print("Found SCTE-35:", scte)
                            print("--------------------------------")
                    except Exception as e:
                        print("ERROR while decoding TS:", e)
                        pass


    def set_socket_options(self, sock):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.MCAST_IP)+socket.inet_aton(self.HOST))
        # TODO: Below is used to specify a specific interface to use for MC subscription

        # group_bin =  socket.inet_aton(self.MCAST_IP)
        # local_bin =  socket.inet_aton(self.IF_IP) # Which interface to IGMP join on

        # sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, local_bin)

        # mreq = struct.pack("4sL", group_bin, socket.INADDR_ANY)
        # # mreq = group_bin + socket.inet_aton('6.116.252.42') # Possible IGMPv3 method

        # sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

if __name__ == "__main__":
    test = TSScte35Parser(mcast_ip="239.0.0.1")
    test.run()
