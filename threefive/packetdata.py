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
        self.pcr_ticks = None
        self.pcr = None
        self.pts_ticks = None
        self.pts = None

    @staticmethod
    def _mk_timestamp(seconds):
        if seconds:
            return round((seconds / 90000.0), 6)
        return seconds

    def mk_pcr(self, table):
        """
        calculates and formats pcr
        """
        try:
            self.pcr_ticks = table[self.program]
            self.pcr = self._mk_timestamp(self.pcr_ticks)
        except:
            pass

    def mk_pts(self, table):
        """
        mk_pts calculates and formats pts
        """
        try:
            self.pts_ticks = table[self.program]
            self.pts = self._mk_timestamp(self.pts_ticks)
        except:
            pass
