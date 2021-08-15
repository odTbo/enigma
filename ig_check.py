from db_connect import *
from ig_connect import Instagram
import re

# Establish DB connection
connection = create_connection()

data = execute_read_query(connection, select_all_query)


def instagram_check():
    instagram_names = []
    for person_data in data:
        socials = person_data[9]
        match = re.search("ig:.*,", socials)
        if match:
            ig_username = match.group().split(":")[1][:-1]
            instagram_names.append(ig_username)

    if len(instagram_names) != 0:
        instagram = Instagram(instagram_names)
        instagram.run()


if __name__ == "__main__":
    instagram_check()
