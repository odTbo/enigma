from birthday_check import BirthdayChecker
from ig_connect import Instagram


def daily_check():
    # Birthday/Nameday Checker
    birthday_checker = BirthdayChecker()
    birthday_checker.run()

    # Instagram Follower/Post-Liker
    instagram = Instagram()
    instagram.run()


if __name__ == "__main__":
    daily_check()
