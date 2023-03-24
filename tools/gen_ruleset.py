import json
import getopt
import sys
sys.path.append('.')
sys.path.append('..')
from pyrsconf import WhoisProxy, RouteSet


def usage():
    print("usage: gen_ruleset.py -a <asn> -m <as-set macro> -p <proto> -o <output-file>")


def get_options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:m:p:o:", ["asn=", "macro=", "proto=", "output="])
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)
        usage()
        sys.exit(2)

    (asn, macro, proto, output) = (None, None, None, None)

    for o, a in opts:
        if o in ("-a", "--asn"):
            asn = a
            if 'AS' in asn:
                asn = asn[2:]
        elif o in ("-m", "--macro"):
            macro = a
        elif o in ("-p", "--proto"):
            proto = a
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"

    if not asn:
        print("Error: insufficient arguments", file=sys.stderr)
        usage()
        sys.exit(2)

    return int(asn), macro, int(proto), output


def main():
    try:
        asn, macro, proto, output = get_options()
        proxy = WhoisProxy()
        routes = []
        if macro is None:
            routes.extend(proxy.expand_as(asn, proto))
        else:
            asn_list = proxy.expand_as_macro(macro)
            for iter_asn in asn_list:
                routes.extend(proxy.expand_as(iter_asn, proto))
            if asn not in asn_list:
                routes.extend(proxy.expand_as(asn, proto))
        route_set = RouteSet.from_list(routes, proto)
        with open(output, "w+") as f:
            f.write(json.dumps(route_set.to_dict(), sort_keys=True, indent=4))
    except Exception as e:
        print(f"Exception caught: {e}", file=sys.stderr)
        exit(1)
    exit(0)


if __name__ == '__main__':
    main()
