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

    @staticmethod
    def _mk_timestamp(seconds):
        if seconds:
            return round((seconds / 90000.0), 6)
        return seconds

    def _chk_table(self, table):
        seconds = None
        if self.program in table:
            seconds = self._mk_timestamp(table[self.program])
        return seconds

    def mk_pcr(self, table):
        """
        calculates and formats pcr
        """
        self.pcr = self._chk_table(table)

    def mk_pts(self, table):
        """
        mk_pts calculates and formats pts
        """
        self.pts = self._chk_table(table)
