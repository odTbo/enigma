import sqlite3
from sqlite3 import Error


# CREATE/ESTABLISH CONNECTION TO DB
def create_connection(path="enigma.db"):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# EXECUTE QUERY
def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False


create_person = """
INSERT INTO
  people (name, surname, email, birthday, nameday, address, interests, phone, socials)
VALUES
  (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

create_data_table = """
CREATE TABLE IF NOT EXISTS people (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  birthday TEXT NOT NULL,
  nameday TEXT,
  address TEXT,
  interests TEXT,
  phone TEXT UNIQUE,
  socials TEXT
);
"""

if __name__ == "__main__":
    # CONNECT TO/CREATE DATABASE
    connection = create_connection()
    # CREATE TABLE
    execute_query(connection, create_data_table)



# params = (name, surname, email, birthday, address, interests, phone, socials)
#
# execute_query(connection, create_person, params)
