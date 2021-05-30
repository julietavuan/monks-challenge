
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
        print("Successfully Connected to SQLite")
    except Error as e:
        print("Failed to connect to sqlite", e)
    return conn


def save(message):
    """
    Create a new monks key value into the monks table
    :param message:
    :return: message id
    """
    conn = None
    try:
        conn = create_connection()
        sql = '''INSERT INTO monks(key, value) VALUES(?,?) '''
        cursor = conn.cursor()
        cursor.execute(sql, (message["key"], message["value"]))
        conn.commit()
        cursor.close()
        return cursor.lastrowid
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


def get(key):
    """
    Get monk value from the giving monk key
    :param key:
    :return: monk key value
    """
    conn = None
    try:
        conn = create_connection()
        sql = '''SELECT key, value FROM monks WHERE key=?'''
        cursor = conn.cursor()
        cursor.execute(sql, (key,))
        return cursor.fetchone()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
