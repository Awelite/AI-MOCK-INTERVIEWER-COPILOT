import os
import mysql.connector

from dotenv import load_dotenv

load_dotenv()


def get_db():

    from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )