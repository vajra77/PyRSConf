from pyrsconf import WhoisProxy


def _generate_routes(asn, asmacro):
    routes = []
    proxy = WhoisProxy()
    if asmacro is None:
        routes.extend(proxy.expand_as(asn))
    else:
        asn_list = proxy.expand_as_macro(asmacro)
        for a in asn_list:
            routes.extend(proxy.expand_as(a))
        if asn not in asn_list:
            routes.extend(proxy.expand_as(asn))
    return routes


class Router:

    def __init__(self, address, asn):
        self._address = address
        self._asn = asn
        self._neighbors = []
        self._filter_bucket = {}

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
        if neigh.asn in self._filter_bucket.keys():
            pass
        else:
            routes = _generate_routes(neigh.asn, neigh.asmacro)
            self._filter_bucket[neigh.asn] = routes
