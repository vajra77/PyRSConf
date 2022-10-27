

PROTO_IPV4 = 4
PROTO_IPV6 = 6


class RouteObject:

    def __init__(self, route, origin, source):
        self._route = route
        self._origin = origin
        self._source = source

    @property
    def route(self):
        return self._route

    @property
    def origin(self):
        return self._origin

    @property
    def source(self):
        return self._source

    def is_inet(self):
        return '.' in self._route

    def is_inet6(self):
        return ':' in self._route

    def proto(self):
        if self.is_inet():
            return PROTO_IPV4
        elif self.is_inet6():
            return PROTO_IPV6
        else:
            raise ValueError("proto unknown")
