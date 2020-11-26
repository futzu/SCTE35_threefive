import io
import socket
import struct
import threefive

''' 
This script has been tested with release 2.2.33 this evening
and has had no issues, errors, problems. 
'''

def foundit(cue):
    print("""\n\t\tthis function was passed into Stream.decode
            it gets called with the cue instance as an arg
            for custom handling when a SCTE-35 packet is found\n""")
            
    print(f'\nCue methods can be called\n\tcue.get_command() returns:\n\t\t\t {cue.get_command()}')
    print(f'\nCue vars can be read.\n\t cue.command.name\n\t\t\t {cue.command.name}')

class StreamFu(threefive.Stream):
    '''
    StreamFu is a subclass of threefive.Stream.
    the _parse_pts method is modified so
    that the video PTS is displayed at the
    bottom of the screen to show progress
    '''

    def _parse_pts(self, pkt, pid):
        """
        parse pts with output
        """
        pts = ((pkt[13] >> 1) & 7) << 30
        pts |= ((pkt[14] << 7) | (pkt[15] >> 1)) << 15
        pts |= (pkt[16] << 7) | (pkt[17] >> 1)
        pts /= 90000.0
        ppp = self._pid_prog[pid]
        self._prog_pts[ppp] = pts
        print(f'PTS: \033[92m{round(pts,3)}\033[0m',end='\r\r\r')

    
        
class MCastParser():
    def __init__(self, mcast_ip, if_ip="0.0.0.0", hostname="0.0.0.0", port=9000):
        self.HOST = hostname
        self.PORT = port
        self.MCAST_IP = mcast_ip
        self.IF_IP = if_ip

    def do(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            self.set_socket_options(sock)
            sock.bind((self.HOST, self.PORT))
            with sock.makefile(mode="rb") as socket_file:
                ts = StreamFu(socket_file)
                ts.decode() # without a function being passed in.

                # other method call examples

                # ts.decode(func=foundit)   # with a function passed in.
                
                # ts.show()   # will display stream types by program.

    def set_socket_options(self, sock):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(self.MCAST_IP)+socket.inet_aton(self.HOST))


if __name__ == "__main__":
    MCastParser(mcast_ip="239.255.0.1").do()

