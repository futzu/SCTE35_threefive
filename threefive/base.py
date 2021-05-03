"""
threefive.base contains
the class SCTE35Base.
"""


class SCTE35Base:
    """
    SCTE35Base is a base class for
    SpliceCommand and SpliceDescriptor classes
    """

    def __repr__(self):
        return str(vars(self))

    def get(self):
        """
        Returns instance as a dict
        """
        return self._kv_clean(vars(self))

    @staticmethod
    def _kv_clean(obj):
        """
        kv_clean removes items from a dict if the value is None
        """
        return {k: v for k, v in obj.items() if v is not None}
