import json
import getopt
import sys
import time
sys.path.append('.')
sys.path.append('..')
from pyrsconf import WhoisProxy, RouteSet
from ixpm import get_customers, get_customer
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
        customers = None
        if do_all:
            customers = get_customers(DB['host'], DB['user'], DB['pass'], DB['name'])
        elif member is not None:
            customers = get_customer(member, DB['host'], DB['user'], DB['pass'], DB['name'])
        else:
            print("specify either -a or -m <ixpm-member> to proceed")
            usage()
            exit(1)

        for cust in customers:
            if proto == 6 and cust.macro6 is not None:
                macro = cust.macro6
            else:
                macro = cust.macro
            file_path = f"{output}/as{cust.asn}-v{proto}.json"
            print(f"generating filters for {cust.name} in: {file_path}")
            sys.stdout.flush()
            try:
                all_routes = WhoisProxy.bulk_expand(cust.asn, macro, proto)
                route_set = RouteSet.from_list(all_routes, proto)
                with open(file_path, "w+") as f:
                    f.write(json.dumps(route_set.to_dict(), sort_keys=True, indent=4))
            except Exception as e:
                print(f"exception caught: {e}", file=sys.stderr)
            finally:
                time.sleep(1.0)
                continue
    except Exception as e:
        print(f"Exception caught: {e}", file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
