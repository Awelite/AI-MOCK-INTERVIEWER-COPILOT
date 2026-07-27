import os
import mysql.connector

from dotenv import load_dotenv

load_dotenv()


def get_db():

    return mysql.connector.connect(

        host="localhost",

        user="root",

        password=os.getenv(
            "MYSQL_PASSWORD"
        ),

        database="ai_interviewer"
    )