from datetime import datetime
from dotenv import load_dotenv
from db_connect import *
import smtplib
import os

load_dotenv()

today = datetime.today()
date = today.strftime("%d/%m")


class BirthdayChecker:
    def __init__(self):
        self.connection = create_connection() # Establish DB connection
        self.data = execute_read_query(self.connection, select_all_query) # Fetch Data
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.email_pass = os.getenv("PASSWORD")
        self.to_email = os.getenv("TO_EMAIL")
        self.mail_content = ""
        self.messages = []
        self.get_notified = False

    def run(self):
        self.check_birthday()
        if self.get_notified:
            self.send_notification_email()
        else:
            print("[Birthday Checker] No birthday/nameday matches found for today.")

    def check_birthday(self):
        """Checks if a person's birthday or nameday in database matches current date."""
        for person_data in self.data:
            full_name = f"{person_data[1]} {person_data[2]}"
            birthday = person_data[4]
            nameday = person_data[5]

            if birthday == date:
                birthday_message = f"Today is {date} and {full_name} has his birthday.\n"
                self.messages.append(birthday_message)
                self.get_notified = True

            if nameday == date:
                nameday_message = f"Today is {date} and {full_name} has his nameday.\n"
                self.messages.append(nameday_message)
                self.get_notified = True

    def send_notification_email(self):
        """Sends personal e-mail notification if anyone has a birthday/nameday."""
        self.mail_content = f"Subject: Birthday/Nameday {date}\n\n"
        for message in self.messages:
            self.mail_content += message

        try:
            print("[Birthday Checker] Sending email...")
            with smtplib.SMTP_SSL("smtp.gmail.com") as server:
                server.login(user=self.sender_email, password=self.email_pass)
                server.sendmail(
                    from_addr=self.sender_email,
                    to_addrs=self.to_email,
                    msg=self.mail_content
                )
        finally:
            print("[Birthday Checker] Done.")


if __name__ == "__main__":
    birthday_checker = BirthdayChecker()
    birthday_checker.run()
