

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
