"""
threefive.base contains
the class SCTE35Base.
"""
import json
from .bitn import NBin


class SCTE35Base:
    """
    SCTE35Base is a base class for
    SpliceCommand and SpliceDescriptor classes
    """

    def __repr__(self):
        return str(vars(self))

    @staticmethod
    def _chk_nbin(nbin):
        if not nbin:
            nbin = NBin()
        return nbin

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

    def load(self, stuff):
        """
        load is used to load
        data from a dict or json string
        """
        if isinstance(stuff, str):
            stuff = json.loads(stuff)
        if isinstance(stuff, dict):
            self.__dict__.update(stuff)

    def _chk_var(self, var_type, nbin_method, var_name, bit_count):
        """
        _chk_var is used to check var values and types before encoding
        """
        var_value = self.__dict__[var_name]
        if var_value is None:
            err_mesg = (
                f"\033[7m{var_name} is not set, it should be type {var_type}\033[27m"
            )
            raise ValueError(err_mesg)
        if not isinstance(var_value, var_type):
            err_mesg = f' \033[7m{var_name} is "{var_value}", it should be type {var_type}\033[27m '
            raise ValueError(err_mesg)
        nbin_method(var_value, bit_count)
