"""
packetdata.py
"""

from .base import SCTE35Base


class PacketData(SCTE35Base):
    """
    A PacketData instance is used
    to hold packet pid, program, pcr and pts
    for SCTE-35 packets.
    """

    def __init__(self, pid, prgm):
        self.pid = hex(pid)
        self.program = prgm
        self.pcr = None
        self.pts = None

    def mk_pcr(self, table):
        """
        calculates and formats pcr
        """
        try:
            pcr_ticks = table[self.program]
            self.pcr = self.as_90k(pcr_ticks)
        except:
            pass

    def mk_pts(self, table):
        """
        mk_pts calculates and formats pts
        """
        try:
            pts_ticks = table[self.program]
            self.pts = self.as_90k(pts_ticks)
        except:
            pass
