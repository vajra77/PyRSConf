import os
import json
import uuid
from pyrsconf import RouteObject


SHARED_RESULTS = dict()


def _get_random_tmpfile():
    return "/tmp/irr-{}.json".format(uuid.uuid4().hex)


class BGPQException(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "bgpq4 error triggered by '{}'.".format(self.message)
        else:
            return "undefined bgpq4 error."


class WhoisProxy:
    """
        Wraps WHOIS operations, relies on bgpq4 and ipwhois
    """
    def __init__(self):
        pass

    # expands an AS-SET into a list of AS numbers, relies on bgpq3
    @classmethod
    def expand_as_macro(cls, macro: str) -> list:
        entries = []
        filename = _get_random_tmpfile()
        cmd = "bgpq4 -h whois.radb.net -t -j {} > {}".format(macro, filename)
        if os.system(cmd) != 0:
            raise BGPQException(macro)
        with open(filename) as f:
            data = json.load(f)
        f.close()
        os.remove(filename)
        for asn in data["NN"]:
            entries.append(int(asn))
        return entries

    # expand an ASN into a list of ROUTE/6 objects
    @classmethod
    def expand_as(cls, asn: int, proto: int) -> list:
        result = []
        filename = _get_random_tmpfile()
        cmd = f"bgpq4 -h whois.radb.net -{proto} -j as{asn} > {filename}"
        if os.system(cmd) != 0:
            raise BGPQException(asn)
        with open(filename) as f:
            data = json.load(f)
        f.close()
        os.remove(filename)

        for net in data['NN']:
            prefix = net['prefix']
            source = "UNDEF"
            route = RouteObject(prefix, asn, source)
            if route.proto() == proto:
                result.append(route)
        return result
