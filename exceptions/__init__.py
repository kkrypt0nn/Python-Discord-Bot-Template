""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn
Description:
This is a template to create your own discord bot in python.

Version: 4.0
"""


class UserBlacklisted(Exception):
    def __init__(self, message="User is blacklisted!"):
        self.message = message
        super().__init__(self.message)


class UserNotOwner(Exception):
    def __init__(self, message="User is not an owner of the bot!"):
        self.message = message
        super().__init__(self.message)
