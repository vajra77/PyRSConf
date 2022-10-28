

class Customer:

    def __init__(self, cid, name, asn, macro, macro6):
        self._id = cid
        self._name = name
        self._asn = asn
        self._macro = macro
        self._macro6 = macro6

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def macro(self):
        return self._macro

    @property
    def macro6(self):
        return self._macro

    @classmethod
    def retrieve_all(cls):
        cnx = mysql.connector.connect(host=DB['host'],
                                      user=DB['user'],
                                      password=DB['password'],
                                      database=DB['database'])
        cursor = cnx.cursor(buffered=True)
        query = None

        if do_all:
            query = "SELECT shortname, autsys, peeringmacro, peeringmacrov6 " \
                    "FROM cust WHERE type <> 2 ORDER BY shortname"
        elif member is not None:
            query = f"SELECT shortname, autsys, peeringmacro, peeringmacrov6 " \
                    f"FROM cust WHERE shortname='{member}'"