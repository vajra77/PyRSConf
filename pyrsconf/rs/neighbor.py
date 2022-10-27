

class Neighbor:

    def __init__(self, address, asn, asmacro, max_prefix):
        self._address = address
        self._asn = asn
        self._asmacro = asmacro
        self._max_prefix = max_prefix

    @property
    def address(self):
        return self._address

    @property
    def asn(self):
        return self._asn

    @property
    def asmacro(self):
        return self._asmacro

    @property
    def max_prefix(self):
        return self._max_prefix