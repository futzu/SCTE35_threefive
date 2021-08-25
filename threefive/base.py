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
        return str(self.get())

    def get(self):
        """
        Returns instance as a dict
        """
        return self.kv_clean()

    def kv_clean(self):
        """
        kv_clean removes items from a dict if the value is None
        """

        def b2l(val):
            if isinstance(val, (SCTE35Base)):
                val.kv_clean()
            if isinstance(val, (list)):
                val = [b2l(v) for v in val]
            if isinstance(val, (dict)):
                val = {k: b2l(v) for k, v in val.items()}
            if isinstance(val, (bytes, bytearray)):
                val = list(val)
            return val

        return {k: b2l(v) for k, v in vars(self).items() if v is not None}
