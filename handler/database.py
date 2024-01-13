# pylint: disable=W0718
# pylint: disable=C0103

"""
Connection handler for PostgresSQL Database
"""

import psycopg2
from .config import db_config


class DataBaseError(Exception):
    """Error during connecting to database"""


conn = None
cur = None
params = db_config()

try:
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    raise DataBaseError


def connect():
    """Connect to database"""
    global conn, cur, params
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as err:
        print(err)
        raise DataBaseError


def check():
    """Check DB Connection"""
    global conn
    try:
        if conn.closed == 0:
            return
        connect()
        return
    except Exception as err:
        print(err)
        raise DataBaseError from err


def insert(table, fields, data, rows=1):
    """Insertion of data to a table"""
    global cur
    query = "INSERT INTO " + table + " "
    columns = ""
    vals = ""
    for i in range(rows):
        columns = columns + fields[i] + ","
    columns = columns[:-1]
    query = query + "(" + columns + ")" + " VALUES "
    for i in range(rows):
        vals = vals + "'"
        vals = vals + data[i] + "'"
        vals = vals + ","
    vals = vals[:-1]
    query = query + "(" + vals + ")"
    # Sending Query
    check()
    cur.execute(query)
    conn.commit()
