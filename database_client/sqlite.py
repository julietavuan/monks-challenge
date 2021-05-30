import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect("monks_database.sqlite")
    except Error as e:
        print(e)
    return conn


def save(conn, message):
    """
    Create a new monks key value into the monks table
    :param message:
    :param conn:
    :return: message id
    """
    sql = '''INSERT INTO monks(key, value) VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (message["key"], message["value"]))
    conn.commit()
    return cur.lastrowid

