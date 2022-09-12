""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.1
"""

import sqlite3

def is_blacklisted(user_id: int) -> bool:
    """
    This function will check if a user is blacklisted.
    
    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM blacklist WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result is not None


def add_user_to_blacklist(user_id: int) -> int:
    """
    This function will add a user based on its ID in the blacklist.
    
    :param user_id: The ID of the user that should be added into the blacklist.
    """
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
    connection.commit()
    rows = cursor.execute("SELECT COUNT(*) FROM blacklist").fetchone()[0]
    connection.close()
    return rows


def remove_user_from_blacklist(user_id: int) -> int:
    """
    This function will remove a user based on its ID from the blacklist.
    
    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
    connection.commit()
    rows = cursor.execute("SELECT COUNT(*) FROM blacklist").fetchone()[0]
    connection.close()
    return rows


def add_warn(user_id: int, server_id: int, moderator_id: int, reason: str) -> int:
    """
    This function will add a warn to the database.
    
    :param user_id: The ID of the user that should be warned.
    :param reason: The reason why the user should be warned.
    """
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    # Get the last `id`
    rows = cursor.execute("SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1", (user_id, server_id,)).fetchone()
    warn_id = rows[0]+1 if rows is not None else 1
    cursor.execute("INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)", (warn_id, user_id, server_id, moderator_id, reason,))
    connection.commit()
    rows = cursor.execute("SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?", (user_id, server_id,)).fetchone()[0]
    connection.close()
    return rows


def remove_warn(warn_id: int, user_id: int, server_id: int) -> int:
    """
    This function will remove a warn from the database.
    
    :param warn_id: The ID of the warn.
    :param user_id: The ID of the user that was warned.
    :param server_id: The ID of the server where the user has been warned
    """
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?", (warn_id, user_id, server_id,))
    connection.commit()
    rows = cursor.execute("SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?", (user_id, server_id,)).fetchone()[0]
    connection.close()
    return rows

def get_warnings(user_id: int, server_id: int) -> list:
    """
    This function will get all the warnings of a user.
    
    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :return: A list of all the warnings of the user.
    """
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?", (user_id, server_id,))
    result = cursor.fetchall()
    connection.close()
    return result