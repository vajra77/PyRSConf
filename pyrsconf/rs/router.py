

class Router:

    def __init__(self, address, asn):
        self._address = address
        self._asn = asn
        self._neighbors = []

    @property
    def address(self):
        return self._address

    @property
    def asn(self):
        return self._asn

    @property
    def neighbors(self):
        return self._neighbors.copy()

    def add_neighbor(self, neigh):
        self._neighbors.append(neigh)
