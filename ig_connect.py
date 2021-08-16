import json
import codecs
import datetime
import time
from os import path, getenv
from db_connect import *
import re
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

load_dotenv()

# https://github.com/ping/instagram_private_api
try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(path.join(path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


class Instagram:
    def __init__(self,):
        self.username = getenv("IG_USERNAME")
        self.password = getenv("IG_PASSWORD")
        self.settings_file_path = "ig_credentials.json"
        self.users = []

    def run(self):
        self.get_users()
        self.login()

        # Threaded follow function
        with ThreadPoolExecutor() as exector:
            exector.map(self.follow_user, self.users)

        # Threaded Posts Liker function
        with ThreadPoolExecutor() as exector:
            exector.map(self.like_all_posts, self.users)

    def login(self):
        # print('Client version: {0!s}'.format(client_version))

        device_id = None
        try:
            settings_file = self.settings_file_path
            if not path.isfile(settings_file):
                # settings file does not exist
                print('Unable to find file: {0!s}'.format(settings_file))

                # login new
                self.api = Client(
                    self.username, self.password,
                    on_login=lambda x: self.onlogin_callback(x, self.settings_file_path), auto_patch=True)
            else:
                with open(settings_file) as file_data:
                    cached_settings = json.load(file_data, object_hook=self.from_json)
                # print('Reusing settings: {0!s}'.format(settings_file))

                device_id = cached_settings.get('device_id')
                # reuse auth settings
                self.api = Client(
                    self.username, self.password,
                    settings=cached_settings, auto_patch=True)

        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

            # Login expired
            # Do relogin but use default ua, keys and such
            self.api = Client(
                self.username, self.password,
                device_id=device_id,
                on_login=lambda x: self.onlogin_callback(x, self.settings_file_path), auto_patch=True)

        except ClientLoginError as e:
            print('ClientLoginError {0!s}'.format(e))
            exit(9)
        except ClientError as e:
            print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
            exit(9)
        except Exception as e:
            print('Unexpected Exception: {0!s}'.format(e))
            exit(99)

        # Show when login expires
        # cookie_expiry = self.api.cookie_jar.auth_expires
        # print('Cookie Expiry: {0!s}'.format(
        #     datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))

    # Get IG Usernames from Database (self.users)
    def get_users(self):
        # Establish DB connection
        connection = create_connection()
        data = execute_read_query(connection, select_all_query)
        for person_data in data:
            socials = person_data[9]
            match = re.search("ig:.*,", socials)
            if match:
                ig_username = match.group().split(":")[1][:-1]
                self.users.append(ig_username)

    # Follow IG User by username
    def follow_user(self, username):
        # Get user_id
        result = self.api.username_info(username)
        user_id = result["user"]["pk"]
        # Follow based on user_id
        r = self.api.friendships_create(user_id)
        if r["status"] == "ok":
            print(f"[IG] Followed {username}.")

    # Like all User's posts
    def like_all_posts(self, username):
        result = self.api.username_info(username)
        user_id = result["user"]["pk"]

        # ---------- Pagination with max_id ----------
        updates = []
        results = self.api.user_feed(user_id)
        updates.extend(results.get('items', []))

        next_max_id = results.get('next_max_id')
        while next_max_id:
            results = self.api.user_feed(user_id, max_id=next_max_id)
            updates.extend(results.get('items', []))
            # if len(updates) >= 30:  # get only first 30 or so
            #     break
            next_max_id = results.get('next_max_id')

        updates.sort(key=lambda x: x['pk'])
        # print list of IDs
        # print(json.dumps([u['pk'] for u in updates], indent=2))

        print(f"[IG] Liking posts for {username}...")
        for post in updates:
            # print(post["pk"], post["id"])
            # Like post
            self.api.post_like(post["id"])
            time.sleep(0.2)
        print(f"[IG] Liked {username}'s all {len(updates)} posts.")

    def to_json(self, python_object):
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': codecs.encode(python_object, 'base64').decode()}
        raise TypeError(repr(python_object) + ' is not JSON serializable')

    def from_json(self, json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object

    def onlogin_callback(self, api, new_settings_file):
        cache_settings = api.settings
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default=self.to_json)
            print('SAVED: {0!s}'.format(new_settings_file))


if __name__ == "__main__":
    ig = Instagram()
    ig.run()
