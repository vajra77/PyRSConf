import os
import json
import uuid
import threading
from pyrsconf import RouteObject


SHARED_RESULTS = dict()


def _get_random_tmpfile():
    return "/tmp/irr-{}.json".format(uuid.uuid4().hex)


def _th_expand_as(asn, proto):
    SHARED_RESULTS[asn] = list()
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
            SHARED_RESULTS[asn].append(route)


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

    @classmethod
    def expand_as_and_macro(cls, asn: int, macro: str, proto: int):
        SHARED_RESULTS.clear()
        grand_result = list()
        asn_list = list()
        if macro is not None:
            asn_list.extend(cls.expand_as_macro(macro))
        if asn not in asn_list:
            asn_list.append(asn)
        threads = list()
        for iter_asn in asn_list:
            th = (threading.Thread(target=_th_expand_as, args=(iter_asn, proto)))
            th.start()
            threads.append(th)
        for th in threads:
            th.join()
        for res in SHARED_RESULTS.values():
            grand_result.extend(res)
        return grand_result
