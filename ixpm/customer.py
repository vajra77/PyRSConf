

class Customer:

    def __init__(self, cid, name, asn, macro, macro6):
        self._id = cid
        self._name = name
        self._asn = asn
        self._macro = macro
        self._macro6 = macro6

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def asn(self):
        return self._asn

    @property
    def macro(self):
        return self._macro

    @property
    def macro6(self):
        return self._macro
