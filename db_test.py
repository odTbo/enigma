import sqlite3
from sqlite3 import Error

db_path = "enigma.db"


# CREATE/ESTABLISH CONNECTION TO DB
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# EXECUTE QUERY
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


connection = create_connection(db_path)

create_data_table = """
CREATE TABLE IF NOT EXISTS people (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  birthday TEXT NOT NULL,
  address TEXT,
  interests TEXT,
  phone TEXT UNIQUE,
  socials TEXT
);
"""

# CREATE TABLE
execute_query(connection, create_data_table)

name = 'First Name'
surname = 'Last Name'
email = 'example@gmail.com'
birthday = '24/12'
address = 'Address 12, Test City'
interests = 'Interests go here.'
phone = '0900666666'
socials = 'Socials go here.'


create_person = """
INSERT INTO
  people (name, surname, email, birthday, address, interests, phone, socials)
VALUES
  (?, ?, ?, ?, ?, ?, ?, ?);
"""
params = (name, surname, email, birthday, address, interests, phone, socials)

execute_query(connection, [create_person, params])