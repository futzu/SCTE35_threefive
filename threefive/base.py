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

    def decode(self):
        """
        decode
        """

    def precheck(self, var_type, nbin_method, var_name, bit_count):
        """
        precheck is used check vars before encoding
        """
        var_value = self.__dict__[var_name]
        if var_value is None:
            raise ValueError(
                f"\033[7m{var_name} is not set, it should be {var_type}\033[27m"
            )
        if not isinstance(var_value, var_type):
            raise Exception(
                f' \033[7m{var_name} is "{var_value}" {type(var_value)}, should be {var_type}\033[27m '
            )
        nbin_method(var_value, bit_count)
