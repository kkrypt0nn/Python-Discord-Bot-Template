""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.0.1
"""

import json


def add_user_to_blacklist(user_id: int):
    with open("blacklist.json", "r+") as file:
        file_data = json.load(file)
        file_data["ids"].append(user_id)
    with open("blacklist.json", "w") as file:
        file.seek(0)
        json.dump(file_data, file, indent=4)


def remove_user_from_blacklist(user_id: int):
    with open("blacklist.json", "r") as file:
        file_data = json.load(file)
        file_data["ids"].remove(user_id)
    with open("blacklist.json", "w") as file:
        file.seek(0)
        json.dump(file_data, file, indent=4)
