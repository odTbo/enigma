from datetime import datetime
from dotenv import load_dotenv
from db_connect import *
import smtplib
import os

load_dotenv()

# Establish DB connection
connection = create_connection()

# Fetch Data
data = execute_read_query(connection, select_all_query)

today = datetime.today()
date = today.strftime("%d/%m")

messages = []
get_notified = False
for person_data in data:
    full_name = f"{person_data[1]} {person_data[2]}"
    birthday = person_data[4]
    nameday = person_data[5]
    if birthday == date:
        birthday_message = f"Today is {date} and {full_name} has his birthday.\n"
        messages.append(birthday_message)
        get_notified = True
    if nameday == date:
        nameday_message = f"Today is {date} and {full_name} has his nameday.\n"
        messages.append(nameday_message)
        get_notified = True

sender_email = os.getenv("SENDER_EMAIL")
email_pass = os.getenv("PASSWORD")
to_email = os.getenv("TO_EMAIL")
mail_content = f"Subject: Birthday/Nameday {date}\n\n"


if get_notified:
    for message in messages:
        mail_content += message
        try:
            print("Sending...")
            with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
                connection.login(user=sender_email, password=email_pass)
                connection.sendmail(
                    from_addr=sender_email,
                    to_addrs=to_email,
                    msg=mail_content
                )
        finally:
            print("Done.")
