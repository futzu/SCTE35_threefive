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
        self.pcr_raw = None
        self.pcr = None
        self.pts_raw = None
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
        self.pcr_raw = table[self.program]
        self.pcr = self._mk_timestamp(self.pcr_raw)

    def mk_pts(self, table):
        """
        mk_pts calculates and formats pts
        """
        self.pts_raw = table[self.program]
        self.pts = self._mk_timestamp(self.pts_raw)
