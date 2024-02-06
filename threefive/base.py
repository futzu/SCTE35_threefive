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

    ROLLOVER = 8589934591

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def as_90k(int_time):
        """
        ticks to 90k timestamps
        """
        return round((int_time / 90000.0), 6)

    @staticmethod
    def as_ticks(float_time):
        """
        90k timestamps to ticks
        """
        return int(round(float_time * 90000))

    @staticmethod
    def as_hms(secs_of_time):
        """
        as_hms converts timestamp to
        00:00:00.000 format
        """
        hours, seconds = divmod(secs_of_time, 3600)
        mins, seconds = divmod(seconds, 60)
        seconds = round(seconds, 3)
        output = f"{int(hours):02}:{int(mins):02}:{seconds:02}"
        if len(output.split(".")[1]) < 2:
            output += "0"
        return output

    @staticmethod
    def fix_hex(hexed):
        """
        fix_hex adds padded zero if needed for byte conversion.
        """
        return (hexed.replace("0x", "0x0", 1), hexed)[len(hexed) % 2 == 0]

    def get(self):
        """
        Returns instance as a dict
        """
        return self.kv_clean()

    def get_json(self):
        """
        get_json returns the instance
        data as json.
        """
        return json.dumps(self.get(), indent=4)

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

    @staticmethod
    def _chk_nbin(nbin):
        if not nbin:
            nbin = NBin()
        return nbin

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
