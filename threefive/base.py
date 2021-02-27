import json
from bitn import NBin


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

    def load(self, stuff):
        """
        load is used to load
        data from a dict or json string
        """
        if isinstance(stuff, str):
            stuff = json.loads(stuff)
        if isinstance(stuff, dict):
            self.__dict__.update(stuff)

    def precheck(self, var_type, nbin_method, var_name, bit_count):
        """
        precheck is used check vars before encoding
        """
        var_value = self.__dict__[var_name]
        if var_value is None:
            raise Exception(
                f"\033[7m{var_name} is not set, it should be type{var_type}\033[27m"
            )
        if not isinstance(var_value, var_type):
            raise Exception(
                f' \033[7m{var_name} is "{var_value}", it should be type {var_type}\033[27m '
            )
        nbin_method(var_value, bit_count)
