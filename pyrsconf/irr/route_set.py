from .route_object import RouteObject


class RouteSet:

    def __init__(self, proto):
        self._proto = proto
        self._routes = []

    @property
    def proto(self):
        return self._proto

    @property
    def routes(self):
        return self._routes.copy()

    def length(self):
        return len(self._routes)

    def add_route(self, route: RouteObject):
        if route.proto() == self.proto:
            self._routes.append(route)
        else:
            raise ValueError(f"route proto mismatch: {route.proto()}")

    def to_dict(self):
        out_routes = []
        for r in self._routes:
            rd = {
                'route': r.route,
                'origin': r.origin,
                'proto': r.proto(),
                'source': r.source
            }
            out_routes.append(rd)
        return {'routes': out_routes}

    @classmethod
    def from_list(cls, routes, proto):
        result = cls(proto)
        for r in routes:
            result.add_route(r)
        return result
