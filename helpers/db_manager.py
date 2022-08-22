""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.0
"""

import sqlite3
import mysql.connector
import os, sys, json

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

def is_blacklisted(user_id: int) -> bool:
    """
    This function will check if a user is blacklisted.
    
    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    connection = set_connection()
    cursor = connection.cursor()
    if config["DATABASE"] == "sqlite3":
        cursor.execute("SELECT * FROM blacklist WHERE user_id= ?", (user_id,))
    elif config["DATABASE"] == 'mysql':
        cursor.execute("SELECT * FROM blacklist WHERE user_id= %s", (user_id,))
            
    result = cursor.fetchone()
    connection.close()
    return result is not None


def add_user_to_blacklist(user_id: int) -> int:
    """
    This function will add a user based on its ID in the blacklist.
    
    :param user_id: The ID of the user that should be added into the blacklist.
    """
    connection = set_connection()
    cursor = connection.cursor()
    
    if config["DATABASE"] == "sqlite3":
        cursor.execute("INSERT INTO blacklist (user_id) VALUES (?)", (user_id,))
    elif config["DATABASE"] == 'mysql':
        cursor.execute("INSERT INTO blacklist (user_id) VALUES (%s)", (user_id,))
        
    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM blacklist")
    (rows,) = cursor.fetchone()
    connection.close()
    return rows


def remove_user_from_blacklist(user_id: int) -> int:
    """
    This function will remove a user based on its ID from the blacklist.
    
    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    connection = set_connection()
    cursor = connection.cursor()
    if config["DATABASE"] == "sqlite3":
        cursor.execute("DELETE FROM blacklist WHERE user_id= ?", (user_id,))
    elif config["DATABASE"] == 'mysql':
        cursor.execute("DELETE FROM blacklist WHERE user_id= %s", (user_id,))
        
    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM blacklist")
    (rows,) = cursor.fetchone()

    connection.close()
    return rows


def add_warn(user_id: int, server_id: int, moderator_id: int, reason: str) -> int:
    """
    This function will add a warn to the database.
    
    :param user_id: The ID of the user that should be warned.
    :param reason: The reason why the user should be warned.
    """
    connection = set_connection()
    cursor = connection.cursor()
    if config["DATABASE"] == "sqlite3":
        cursor.execute("INSERT INTO warns (user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?)", (user_id, server_id, moderator_id, reason))
        connection.commit()
        cursor.execute("SELECT COUNT(*) FROM warns WHERE user_id= ? AND server_id= ?", (user_id, server_id,))
    elif config["DATABASE"] == 'mysql':
        cursor.execute("INSERT INTO warns (user_id, server_id, moderator_id, reason) VALUES (%s, %s, %s, %s)", (user_id, server_id, moderator_id, reason))
        connection.commit()
        cursor.execute("SELECT COUNT(*) FROM warns WHERE user_id= %s AND server_id= %s", (user_id, server_id,))
    (rows,) = cursor.fetchone()

    connection.close()
    return rows


def get_warnings(user_id: int, server_id: int) -> list:
    """
    This function will get all the warnings of a user.
    
    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :return: A list of all the warnings of the user.
    """
    connection = set_connection()
    cursor = connection.cursor()
    if config["DATABASE"] == "sqlite3":
        cursor.execute("SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at) FROM warns WHERE user_id=? AND server_id=?", (user_id, server_id,))
    elif config["DATABASE"] == 'mysql':
        cursor.execute("SELECT user_id, server_id, moderator_id, reason, created_at FROM warns WHERE user_id=%s AND server_id=%s", (user_id, server_id,))
    result = cursor.fetchall()
    connection.close()
    return result

def set_connection():
    if config["DATABASE"] == "sqlite3":
        return sqlite3.connect("database/database.db")
    elif config["DATABASE"] == "mysql":
        return mysql.connector.connect(
            user = config["DB_USER"], 
            host = config["DB_HOST"], 
            password = config["DB_PASSWORD"], 
            port = config["DB_PORT"], 
            database = config["DB_NAME"]
        )
        