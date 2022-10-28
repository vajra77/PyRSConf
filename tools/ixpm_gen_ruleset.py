import json
import getopt
import threading
import mysql.connector
import sys
sys.path.append('.')
sys.path.append('..')
from pyrsconf import WhoisProxy, RouteSet
from config import DB


SHARED_SEMAPHORE = threading.Semaphore(4)


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
            query = "SELECT shortname, autsys, peeringmacro, peeringmacrov6 FROM cust ORDER BY shortname"
        elif member is not None:
            query = f"SELECT shortname, autsys, peeringmacro, peeringmacrov6 FROM cust WHERE shortname='{member}'"
        else:
            print("specify either -a or -m <ixpm-member> to proceed")
            cursor.close()
            cnx.close()
            usage()
            exit(1)

        cursor.execute(query)
        for (name, asn, macro4, macro6) in cursor:
            if proto == 6 and macro6 is not None:
                macro = macro6
            else:
                macro = macro4
            file_path = f"{output}/as{asn}-v{proto}.json"
            print(f"generating filters for {name} in: {file_path}")
            sys.stdout.flush()
            try:
                SHARED_SEMAPHORE.acquire()
                all_routes = WhoisProxy.bulk_expand(asn, macro, proto)
                SHARED_SEMAPHORE.release()

                route_set = RouteSet.from_list(all_routes, proto)
                with open(file_path, "w+") as f:
                    f.write(json.dumps(route_set.to_dict(), sort_keys=True, indent=4))
            except Exception as e:
                print(f"exception caught: {e}", file=sys.stderr)
                SHARED_SEMAPHORE.release()
            # finally:
            #     continue
        cursor.close()
        cnx.close()
    except Exception as e:
        print(f"Exception caught: {e}", file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
