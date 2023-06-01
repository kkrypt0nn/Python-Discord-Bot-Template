import os
import psycopg2

""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
async def get_blacklisted_users() -> list:
    """
    This function will return the list of all blacklisted users.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, created_at FROM blacklist"
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]


async def is_blacklisted(user_id: int) -> bool:
    """
    This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
        
    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM blacklist WHERE user_id=%s", (str(user_id),)
                )
                result = cursor.fetchall()
                return len(result) > 0
        # Als er iets misgaat, geven we geen toegang tot de bot
        except:
            return True
        

async def add_user_to_blacklist(user_id: int) -> int:
    """
    This function will add a user based on its ID in the blacklist.

    :param user_id: The ID of the user that should be added into the blacklist.
    """

    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute("INSERT INTO blacklist(user_id) VALUES (%s)", (str(user_id),))
                con.commit()
                cursor.execute("SELECT COUNT(*) FROM blacklist")
                result = cursor.fetchone()
                return result[0] if result is not None else 0
            
    except:
        return -1


async def remove_user_from_blacklist(user_id: int) -> int:
    """
    This function will remove a user based on its ID from the blacklist.

    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute("DELETE FROM blacklist WHERE user_id=%s", (str(user_id),))
                con.commit()
                cursor.execute("SELECT COUNT(*) FROM blacklist")
                result = cursor.fetchone()
                return result[0] if result is not None else 0
            
    except:
        return -1


async def get_ooc_messages(limit: int) -> list:
    """
    This function will return a list of random ooc messages.

    :param limit: The amount of randomy selected messages
    """
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT message_id, added_at, added_by, times_played FROM context_message ORDER BY random() LIMIT %s", (limit,)
                )
                return cursor.fetchall()
            
    except Exception as err:
        print(err)
        return [-1, err]
    
async def get_ooc_message(id) -> list:
    """
    This function will return a list of random ooc messages.

    :param limit: The amount of randomy selected messages
    """
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT message_id, added_at, added_by, times_played FROM context_message WHERE message_id=%s", (str(id),)
                )
                return cursor.fetchall()
            
    except Exception as err:
        print(err)
        return [-1, err]


async def is_in_ooc(message_id: int) -> bool:
    """
    This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
        
    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM context_message WHERE message_id=%s", (str(message_id),)
                )
                result = cursor.fetchall()
                return len(result) > 0
        # Als er iets misgaat, zeggen we dat bericht al in db zit
        except:
            return True
        

async def increment_times_played(message_id):
    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "UPDATE context_message SET times_played = times_played + 1 WHERE message_id=%s", (str(message_id),)
                )
                con.commit()
                return True

        except:
            return False


async def add_message_to_ooc(message_id:int, added_by:int) -> int:
    """
    This function will add a OOC message based on its ID in the blacklist.

    :param message_id: The ID of the message that should be added.
    :param added_by: The ID of the user who submitted the message.
    :param about: The ID of the user whom the message is about.

    """

    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO context_message(message_id, added_by) VALUES (%s, %s)",
                    (str(message_id), str(added_by),)
                )
                con.commit()
                cursor.execute("SELECT COUNT(*) FROM context_message")
                result = cursor.fetchone()
                return result[0] if result is not None else 0
    except Exception as err:
        print(err)
        return -1


async def remove_message_from_ooc(message_id: int) -> int:
    """
    This function will remove a message based on its ID from the ooc game.

    :param message_id: The ID of the message that should be removed from the game.
    """
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute("DELETE FROM context_message WHERE message_id=%s", (str(message_id),))
                con.commit()
                cursor.execute("SELECT COUNT(*) FROM context_message")
                result = cursor.fetchone()
                return result[0] if result is not None else 0
            
    except:
        return -1
    
