import os
import psycopg2

""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
# TODO voeg try catch toe
async def get_blacklisted_users() -> list:
    """
    This function will return the list of all blacklisted users.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        with con.cursor() as cursor:
            cursor.execute(
                "SELECT user_id, created_at FROM blacklist"
            )
            return cursor.fetchall()


async def is_blacklisted(user_id: int) -> bool:
    """
    This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
        
    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        with con.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM blacklist WHERE user_id=%s", (str(user_id),)
            )
            result = cursor.fetchall()
            return len(result) > 0
        

async def add_user_to_blacklist(user_id: int) -> int:
    """
    This function will add a user based on its ID in the blacklist.

    :param user_id: The ID of the user that should be added into the blacklist.
    """


    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
         with con.cursor() as cursor:
            cursor.execute("INSERT INTO blacklist(user_id) VALUES (%s)", (str(user_id),))
            con.commit()
            cursor.execute("SELECT COUNT(*) FROM blacklist")
            result = cursor.fetchone()
            return result[0] if result is not None else 0


async def remove_user_from_blacklist(user_id: int) -> int:
    """
    This function will remove a user based on its ID from the blacklist.

    :param user_id: The ID of the user that should be removed from the blacklist.
    """

    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM blacklist WHERE user_id=%s", (str(user_id),))
            con.commit()
            cursor.execute("SELECT COUNT(*) FROM blacklist")
            result = cursor.fetchone()
            return result[0] if result is not None else 0
