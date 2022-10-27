import json
import getopt
import mysql.connector
import sys
sys.path.append('.')
sys.path.append('..')
from pyrsconf import WhoisProxy, RouteSet
from config import DB


def usage():
    print("usage: ixpm_gen_ruleset.py -c <config-file> [-a | -m <ixpm-member>] -o <output-dir>")


def get_options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "am:p:o:", ["member=", "proto=", "output="])
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)
        usage()
        sys.exit(2)

    (do_all, member, proto, output) = (None, False, None, None)

    for o, a in opts:
        if o in ("-a", "--all"):
            do_all = True
        elif o in ("-m", "--member"):
            member = a
        elif o in ("-p", "--proto"):
            proto = a
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"

    return do_all, member, int(proto), output


def main():
    try:
        do_all, member, proto, output = get_options()

        cnx = mysql.connector.connect(host=DB['host'],
                                      user=DB['user'],
                                      password=DB['password'],
                                      database=DB['database'])
        cursor = cnx.cursor(buffered=True)
        query = None

        if do_all:
            query = "SELECT shortname, autsys, peeringmacro FROM cust ORDER BY shortname"
        elif member is not None:
            query = f"SELECT shortname, autsys, peeringmacro FROM cust WHERE shortname='{member}'"
        else:
            print("specify either -a or -m <ixpm-member> to proceed")
            usage()
            exit(1)

        cursor.execute(query)
        proxy = WhoisProxy()
        for (name, asn, macro) in cursor:
            file_path = f"{output}/as{asn}-v{proto}.json"
            print(f"generating filters for {name} in: {file_path}")
            routes = []
            try:
                if macro is None:
                    routes.extend(proxy.expand_as(asn, proto))
                else:
                    asn_list = proxy.expand_as_macro(macro)
                    for iter_asn in asn_list:
                        routes.extend(proxy.expand_as(iter_asn, proto))
                    if asn not in asn_list:
                        routes.extend(proxy.expand_as(asn, proto))
                route_set = RouteSet.from_list(proto, routes)
                with open(file_path, "w+") as f:
                    f.write(json.dumps(route_set.to_dict(), sort_keys=True, indent=4))
            except Exception as e:
                print(f"exception caught: {e}", file=sys.stderr)
            finally:
                continue

    except Exception as e:
        print(f"Exception caught: {e}", file=sys.stderr)
        exit(1)
    exit(0)


if __name__ == '__main__':
    main()
