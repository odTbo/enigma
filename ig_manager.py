from db_connect import *
import re

# Establish DB connection
connection = create_connection()

data = execute_read_query(connection, select_all_query)

instagram_names = []
for person_data in data:
    socials = person_data[9]
    ig_name = re.search("ig:.*,", socials)
    if ig_name:
        ig_name = ig_name.group().split(":")[1][:-1]
        instagram_names.append(ig_name)

if len(instagram_names) == 0:
    print("No IG accounts found.")
else:
    for name in instagram_names:
        print(name)
