from .customer import Customer
import mysql.connector


def get_customers(db_host, db_user, db_pass, db_name):
    result = list()
    cnx = mysql.connector.connect(host=db_host,
                                  user=db_user,
                                  password=db_pass,
                                  database=db_name)
    cursor = cnx.cursor(buffered=True)
    query = "SELECT id,shortname,autsys,peeringmacro,peeringmacrov6 " \
            "FROM cust WHERE type <> 2 ORDER BY shortname"
    cursor.execute(query)
    for (cid, name, asn, macro4, macro6) in cursor:
        result.append(Customer(cid, name, asn, macro4, macro6))
    cursor.close()
    cnx.close()
    return result


def get_customer(c_name, db_host, db_user, db_pass, db_name):
    result = list()
    cnx = mysql.connector.connect(host=db_host,
                                  user=db_user,
                                  password=db_pass,
                                  database=db_name)
    cursor = cnx.cursor(buffered=True)
    query = f"SELECT id,shortname,autsys,peeringmacro,peeringmacrov6 " \
            f"FROM cust WHERE shorthname={c_name}"
    cursor.execute(query)
    for (cid, name, asn, macro4, macro6) in cursor:
        result.append(Customer(cid, name, asn, macro4, macro6))
    cursor.close()
    cnx.close()
    return result
