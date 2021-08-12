from datetime import datetime
from db_connect import *

# Establish DB connection
connection = create_connection()

data = execute_read_query(connection, select_all_query)

today = datetime.today()
date = today.strftime("%d/%m")

no_tasks = True
for person_data in data:
    full_name = f"{person_data[1]} {person_data[2]}"
    birthday = person_data[4]
    nameday = person_data[5]
    if birthday == date:
        print(f"Today is {date} and {full_name} has his birthday.")
        no_tasks = False
    if nameday == date:
        print(f"Today is {date} and {full_name} has his nameday.")
        no_tasks = False


if no_tasks:
    print("No friend has birthday today.")